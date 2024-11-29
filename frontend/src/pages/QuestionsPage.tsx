import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from "@/components/ui/accordion"
import SidebarLayout from "@/layouts/layout.tsx";
import React from "react";
import TitlePage from "@/components/Base/TitlePage.tsx";

const QuestionsPage: React.FC = () => {
    return (
        <SidebarLayout>
            <TitlePage text="Часто задаваемые вопросы"/>
            <Accordion type="single" collapsible className="w-[85vw] max-w-2xl mx-auto mb-5">
                <AccordionItem value="item-1">
                    <AccordionTrigger>Как зарегистрироваться и авторизоваться в боте и на сайте?</AccordionTrigger>
                    <AccordionContent>
                        Для авторизации в боте вам необходимо ввести свой адрес электронной почты и пароль. Веб-приложение автоматически авторизуется за вас, если вы уже вошли в бота. Также вы можете пройти процесс авторизации самостоятельно через веб-интерфейс.
                    </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-2">
                    <AccordionTrigger>Как создать новую ВКС?</AccordionTrigger>
                    <AccordionContent>
                        Для создания новой ВКС перейдите на страницу "Создать мероприятие" и заполните обязательные поля: название, дату и время начала, продолжительность, участников и средство проведения. После заполнения приложение отправит информацию в систему.
                    </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-3">
                    <AccordionTrigger>Как я могу найти предстоящие видеоконференции?</AccordionTrigger>
                    <AccordionContent>
                        Перейдите на страницу "Все мероприятия", чтобы выбрать дату, и переключите фильтр состояния на "Запланированные". Если фильтры не указаны, приложение покажет все ВКС за выбранный период.
                    </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-4">
                    <AccordionTrigger>Как узнать, в каких ВКС я являюсь участником?</AccordionTrigger>
                    <AccordionContent>
                        Откройте страницу "Мои мероприятия". На ней также доступны фильтры для удобного отображения данных, чтобы быстро найти нужные вам ВКС.
                    </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-5">
                    <AccordionTrigger>Где я могу найти ссылку для подключения к видеоконференции?</AccordionTrigger>
                    <AccordionContent>
                        Нажмите на мероприятие, чтобы посмотреть подробную информацию о нём. Ссылка для подключения будет отображаться только для тех ВКС, в которых вы являетесь участником. Она будет предоставлена после поиска или создания ВКС.
                    </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-6">
                    <AccordionTrigger>Как изменить или отменить запланированную ВКС?</AccordionTrigger>
                    <AccordionContent>
                        В текущей версии приложения функционал изменения и отмены ВКС отсутствует. Для этого вам необходимо обратиться к администратору системы.
                    </AccordionContent>
                </AccordionItem>
            </Accordion>
        </SidebarLayout>
    )
}

export default QuestionsPage;