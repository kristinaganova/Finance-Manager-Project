## Finance-Manager-Project

#Описание на Проекта
Финансов Мениджър е настолно приложение, създадено за управление на лични финанси. Приложението предоставя функционалности за проследяване на транзакции, управление на цели за спестяване, както и управление на различни методи на плащане като банкови карти и пари в брой. В допълнение, приложението предлага визуализации и отчети, които помагат на потребителя да разбере по-добре своите финанси и да планира бъдещето си.

#Основни Функционалности
1. Управление на Потребители <br />
Регистрация: Позволява на нови потребители да създадат акаунт с потребителско име и парола.
Вход: Позволява на съществуващи потребители да влязат в акаунта си чрез потребителско име и парола.
Потребителски Данни: Всеки потребител има свои собствени данни за транзакции, цели и методи на плащане, които са защитени и достъпни само за него.
2. Управление на Транзакции <br />
Добавяне на Транзакции: Потребителят може да добавя нови транзакции, като избира дата, категория, сума, тип (приход или разход), метод на плащане и валута. <br />
Изтриване на Транзакции: Потребителят може да изтрие съществуваща транзакция, като съответно актуализира баланса на свързания метод на плащане. <br />
Визуализация на Транзакции: Потребителят може да види всички свои транзакции във формата на таблица и да получи различни визуализации като графики за разпределение на разходите, времеви серии и други.
3. Управление на Методи на Плащане <br />
Добавяне на Метод на Плащане: Потребителят може да добавя нови методи на плащане (напр. нова карта или пари в брой), като задава име, тип и начален баланс. <br />
Изтриване на Метод на Плащане: Потребителят може да изтрива съществуващи методи на плащане. Ако методът на плащане е свързан с някаква цел, тя също ще бъде актуализирана.
Проследяване на Баланси: Потребителят може да следи текущите баланси на всичките си методи на плащане.
4. Управление на Финансови Цели <br />
Добавяне на Цели: Потребителят може да създава финансови цели с име, целева сума, крайна дата и начален депозит.
Добавяне на Сума към Цел: Потребителят може да добавя суми към съществуваща цел от определен метод на плащане.
Изтриване на Цели: Потребителят може да изтрива цели. Балансът на целта може да бъде прехвърлен обратно в метода на плащане.
Проследяване на Напредък: Потребителят може да проследява напредъка на своите цели чрез визуализации като графики и индикатори.
5. Визуализации и Отчети <br />
Статистически Отчети: Потребителят може да генерира статистически отчети за своите транзакции, включително средни стойности, медиана и стандартно отклонение.
Корелации: Възможност за анализ на корелациите между различни категории разходи.
Прогнозиране: Потребителят може да получи прогнози за бъдещи приходи и разходи въз основа на исторически данни.
Клъстеризация: Анализ на транзакциите чрез клъстеризация с цел откриване на тенденции.
Технологии
Програмен Език: Python
GUI: Tkinter
База Данни: SQLite
Пакети за Визуализация: Matplotlib, Seaborn, Plotly
Криптиране на Пароли: bcrypt

#Структура на Проекта <br />
finance_manager/ <br />
├── core/ <br />
│ ├── account_manager.py <br />
│ ├── currency_converter.py <br />
│ ├── finance_manager.py <br />
│ ├── goal_manager.py
│ ├── transaction_manager.py <br />
│ └── user.py <br />
├── ui/ <br />
│ ├── gui.py <br />
│ ├── goal_window.py <br />
│ ├── transaction_window.py <br />
│ ├── payment_method_window.py <br />
├── utils/ <br />
│ ├── initialize_database.py <br />
└── README.md <br />

#Основни Модули <br />
core/account_manager.py: Управлява методите на плащане и баланса им. <br />
core/currency_converter.py: Обработва конвертирането на валути. <br />
core/finance_manager.py: Централен мениджър, който интегрира всички други мениджъри. <br />
core/goal_manager.py: Управлява финансовите цели на потребителя. <br />
core/transaction_manager.py: Управлява транзакциите на потребителя. <br />
core/user.py: Управлява регистрацията и входа на потребителите. <br />
ui/gui.py: Основният GUI на приложението. <br />
ui/goal_window.py: GUI за управление на цели. <br />
ui/transaction_window.py: GUI за управление на транзакции. <br />
ui/payment_method_window.py: GUI за управление на методи на плащане. <br />
utils/initialize_database.py: Инициализира базата данни при първоначално стартиране. <br />