import React from 'react';
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from 'react-hook-form';
import { z } from "zod";
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage
} from "../components/ui/form.tsx";
import { Button } from "@/components/ui/button.tsx";
import { Input } from "@/components/ui/input.tsx";
import { AuthResponse } from "@/types/Auth.ts";
import { useNavigate } from "react-router";
import { getRefreshToken } from "@/utils/decodeToken.ts";
import AuthService from "@/services/AuthService.ts";
import axios from 'axios'; // Импортируем axios для HTTP-запросов

const formSchema = z.object({
    login: z.string().email({
        message: "Введите корректный адрес электронной почты.",
    }),
    password: z.string().min(2, {
        message: "Пароль должен состоять как минимум из 2 символов.",
    }),
});

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


    // Тестовые сервис входа через телеграм-бота
    const initData = window.Telegram.WebApp.initData;
    const userParam = new URLSearchParams(initData).get('user');
    let userId = 0;

    const fetchUserJWT = async (id: number) => {
        try {
            const response = await axios.get(`https://uylg2k-46-39-4-44.ru.tuna.am/users_jwt/${id}`);
            if (response.status === 200) {
                const userJwt = response.data.user_jwt;
                localStorage.setItem('token', userJwt);
                navigate("/meetings");
                return userJwt;
            }
        } catch (error) {
            console.error('Ошибка при получении user JWT:', error);
        }
    };

    React.useEffect(() => {
        const initializeUser = async () => {
            if (userParam) {
                try {
                    const user = JSON.parse(userParam);
                    userId = user.id;
                    if (userId) {
                        await fetchUserJWT(userId);
                    }
                } catch (error) {
                    console.error('Не удалось получить userId:', error);
                }
            } else {
                console.error('Не существует параметра userData.');
            }
        };

        initializeUser();
    }, [userParam]);

    const onSubmit = async (values: z.infer<typeof formSchema>) => {
        setLoading(true);
        try {
            const response = await AuthService.login(values.login, values.password);
            const authData: AuthResponse = response.data;
            localStorage.setItem('token', authData.token);
            localStorage.setItem('refreshToken', getRefreshToken(authData.token));

            navigate("/meetings");
        } catch (error) {
            console.error('Ошибка:', error);
            form.setError('login', { message: 'Неверная почта или пароль!' });
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
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Почта</FormLabel>
                                <FormControl>
                                    <Input placeholder="Почта" {...field} />
                                </FormControl>
                                <FormDescription>
                                    Тестовая почта hantaton10.h@mail.ru
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="password"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Пароль</FormLabel>
                                <FormControl>
                                    <Input type={"password"} placeholder="Пароль" {...field} />
                                </FormControl>
                                <FormDescription>
                                    Тестовый пароль 14Jiuqnr1sWWvo6G
                                </FormDescription>
                                <FormMessage />
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
