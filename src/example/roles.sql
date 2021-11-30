CREATE USER  customer WITH password 'customer';
CREATE USER trainer WITH password 'trainer';
CREATE USER machine WITH password 'machine';
CREATE USER manager WITH password 'manager';

GRANT USAGE ON SCHEMA "gym" TO customer;
GRANT USAGE ON SCHEMA "gym" TO trainer;
GRANT USAGE ON SCHEMA "gym" TO machine;
GRANT USAGE ON SCHEMA "gym" TO manager;

--Courses
GRANT SELECT ON TABLE "gym".courses TO customer;
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".courses TO trainer;
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".courses TO manager;

--Lessons
GRANT SELECT ON TABLE "gym".courses TO customer;
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".lessons TO trainer;
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".lessons TO manager;

--Reservations
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".reservations TO customer;
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".reservations TO trainer;
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".reservations TO manager;

--Lesson Reservations
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".lesson_reservation TO customer;
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".lesson_reservation TO trainer;
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".lesson_reservation TO manager;

--Weight Room Reservations
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".weight_room_reservations TO customer;
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".weight_room_reservations TO trainer;
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".weight_room_reservations TO manager;

--Slots
GRANT SELECT ON TABLE "gym".slots TO customer;
GRANT SELECT ON TABLE "gym".slots TO trainer;
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".slots TO manager;

--Accesses
GRANT SELECT ON TABLE "gym".accesses TO customer;
GRANT SELECT ON TABLE "gym".accesses TO trainer;
GRANT INSERT, UPDATE ON TABLE "gym".accesses TO machine;
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".accesses TO manager;

--Policies
GRANT SELECT ON TABLE "gym".policies TO customer;
GRANT SELECT ON TABLE "gym".policies TO trainer;
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".policies TO manager;

--Users
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".users TO customer;
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".users TO trainer;
GRANT SELECT ON TABLE "gym".users TO machine;--cosi riesce a gestire le Transaction, sa gia che l'abbon. è valido perche si trova oltre il varco della palestra
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".users TO manager;

--Subscriptions
GRANT UPDATE, SELECT ON TABLE "gym".subscriptions TO customer;
GRANT UPDATE, SELECT ON TABLE "gym".subscriptions TO trainer;
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".subscriptions TO manager;

--Transactions
GRANT SELECT ON TABLE "gym".transactions TO customer;
GRANT SELECT ON TABLE "gym".transactions TO trainer;
GRANT INSERT ON TABLE "gym".transactions TO machine;
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE "gym".transactions TO manager;

