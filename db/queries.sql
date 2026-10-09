-- Все заявки со статусом и категорией
SELECT r.Id, r.Title, s.Name AS Status, c.Name AS Category
FROM Requests r
JOIN Statuses s ON r.StatusId = s.Id
JOIN Categories c ON r.CategoryId = c.Id;

-- Заявки конкретного исполнителя
SELECT r.Id, r.Title, s.Name
FROM Requests r
JOIN Statuses s ON r.StatusId = s.Id
WHERE r.AssigneeId = 3;

-- Количество заявок по статусам
SELECT s.Name, COUNT(r.Id) AS Cnt
FROM Statuses s
LEFT JOIN Requests r ON r.StatusId = s.Id
GROUP BY s.Id;

-- Все заявки заявителя user1
SELECT Id, Title, CreatedAt FROM Requests WHERE AuthorId = 4;

-- Поиск заявок по слову
SELECT Id, Title FROM Requests WHERE Title LIKE '%проектор%';

-- Обновить статус заявки
UPDATE Requests SET StatusId = 3 WHERE Id = 2;

-- Изменить ФИО пользователя
UPDATE Users SET FullName = 'Иванов Иван Иванович' WHERE Id = 1;

-- Удалить комментарий
DELETE FROM Comments WHERE Id = 5;

-- Удалить запись истории
DELETE FROM RequestHistory WHERE Id = 3;