INSERT INTO Roles (Name) VALUES 
('Администратор'), ('Оператор'), ('Исполнитель'), ('Заявитель');

INSERT INTO Statuses (Name) VALUES 
('Новая'), ('В работе'), ('Выполнена'), ('Закрыта');

INSERT INTO Categories (Name) VALUES 
('Оборудование'), ('Программное обеспечение'), ('Доступ'), ('Прочее');

INSERT INTO Users (Login, PasswordHash, FullName, RoleId) VALUES
('admin', 'hash1', 'Иванов И.И.', 1),
('operator', 'hash2', 'Петров П.П.', 2),
('executor', 'hash3', 'Сидоров А.А.', 3),
('user1', 'hash4', 'Смирнова А.В.', 4);

INSERT INTO Requests (Title, Description, AuthorId, AssigneeId, StatusId, CategoryId) VALUES
('Не работает проектор', 'В аудитории 305 не включается проектор', 4, 3, 2, 1),
('Установить Python', 'Нужен Python 3.12 для учёбы', 4, 3, 3, 2),
('Доступ к Wi-Fi', 'Не подключается к корпоративной сети', 4, NULL, 1, 3),
('Заменить лампу', 'Перегорела лампа в аудитории 210', 4, 3, 3, 1),
('Обновить 1С', 'Требуется обновление до последней версии', 4, NULL, 1, 2);

INSERT INTO Comments (RequestId, UserId, Text) VALUES
(1, 3, 'Принял в работу, посмотрю сегодня'),
(1, 4, 'Спасибо, жду'),
(2, 3, 'Установил, проверьте'),
(2, 4, 'Всё работает, спасибо'),
(3, 2, 'Передал в сетевой отдел');

INSERT INTO RequestHistory (RequestId, ChangedBy, OldStatusId, NewStatusId) VALUES
(1, 3, 1, 2),
(2, 3, 2, 3),
(4, 3, 2, 3);