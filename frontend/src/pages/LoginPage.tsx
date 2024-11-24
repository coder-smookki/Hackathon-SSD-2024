import React from 'react';
import {zodResolver} from "@hookform/resolvers/zod";
import {useForm} from 'react-hook-form';
import {z} from "zod"
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage
} from "../components/ui/form.tsx";
import {Button} from "@/components/ui/button.tsx";
import {Input} from "@/components/ui/input.tsx";
import {AuthResponse} from "@/types/Auth.ts";
import {useNavigate} from "react-router";
import {getRefreshToken} from "@/utils/decodeToken.ts";
import AuthService from "@/services/AuthService.ts";

const formSchema = z.object({
    login: z.string().min(2, {
        message: "Логин должен состоять как минимум из 2 символов.",
    }),
    password: z.string().min(2, {
        message: "Пароль должен состоять как минимум из 2 символов.",
    }),
})

const LoginPage: React.FC = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = React.useState(false);

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            login: "",
            password: "",
        },
    });

    const onSubmit = async (values: z.infer<typeof formSchema>) => {
        setLoading(true);
        try {
            const response = await AuthService.login(values.login, values.password);
            const authData: AuthResponse = response.data;
            localStorage.setItem('token', authData.token);
            localStorage.setItem('refreshToken', getRefreshToken(authData.token));
            navigate("/events");
        } catch (error) {
            console.error('Ошибка:', error);
            form.setError('login', {message: 'Неверный логин или пароль!'});
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={"h-screen flex flex-col justify-center items-center"}>
            <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl mb-10 text-center">
                Вход в систему
            </h1>

            <Form {...form}>
                <form
                    onSubmit={form.handleSubmit(onSubmit)}
                    className={"flex flex-col justify-center space-y-8 min-w-[min(300px,80vw)] mx-auto"}
                >
                    <FormField
                        control={form.control}
                        name="login"
                        render={({field}) => (
                            <FormItem>
                                <FormLabel>Логин</FormLabel>
                                <FormControl>
                                    <Input placeholder="Логин" {...field} />
                                </FormControl>
                                <FormDescription>
                                    Тестовый логин Hantaton01
                                </FormDescription>
                                <FormMessage/>
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="password"
                        render={({field}) => (
                            <FormItem>
                                <FormLabel>Пароль</FormLabel>
                                <FormControl>
                                    <Input type={"password"} placeholder="Пароль" {...field} />
                                </FormControl>
                                <FormDescription>
                                    Тестовый пароль t6vYHnNhBqN1F4(q
                                </FormDescription>
                                <FormMessage/>
                            </FormItem>
                        )}
                    />
                    <Button type="submit" disabled={loading}>
                        {loading ? 'Загрузка...' : 'Войти'}
                    </Button>
                </form>
            </Form>
        </div>
    );
};

export default LoginPage;