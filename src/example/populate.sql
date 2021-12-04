DROP VIEW IF EXISTS gym.slots_with_current_reservation_V;
CREATE VIEW gym.slots_with_current_reservation_V AS
    SELECT s.*, count(w.*) as current_reservations FROM gym.slots s left join gym.weight_room_reservations w on s.id = w.slot
    group by id, date, time_from, time_to, max_capacity;

INSERT INTO gym.slots values (gen_random_uuid(),'2021-12-25', '08:00:00', '12:00:00', 60, 'Titolo Slot', 'Descrizione slot');
INSERT INTO gym.slots values (gen_random_uuid(),'2021-12-25', '12:00:00', '16:00:00', 80, 'Titolo Slot', 'Descrizione slot');
INSERT INTO gym.slots values (gen_random_uuid(),'2021-12-25', '16:00:00', '20:00:00', 90, 'Titolo Slot', 'Descrizione slot');
INSERT INTO gym.slots values (gen_random_uuid(),'2021-12-23', '08:00:00', '12:00:00', 60, 'Titolo Slot', 'Descrizione slot');
INSERT INTO gym.slots values (gen_random_uuid(),'2021-12-23', '12:00:00', '16:00:00', 80, 'Titolo Slot', 'Descrizione slot');
INSERT INTO gym.slots values (gen_random_uuid(),'2021-12-22', '10:00:00', '11:00:00', 90, 'Titolo Slot', 'Descrizione slot');
INSERT INTO gym.slots values (gen_random_uuid(),'2021-12-21', '08:00:00', '12:00:00', 10, 'Titolo Slot', 'Descrizione slot');
INSERT INTO gym.slots values (gen_random_uuid(),'2021-12-21', '12:00:00', '16:00:00', 20, 'Titolo Slot', 'Descrizione slot');
INSERT INTO gym.slots values (gen_random_uuid(),'2021-12-21', '16:00:00', '20:00:00', 30, 'Titolo Slot', 'Descrizione slot');

INSERT INTO gym.users (id, name, surname, birth_date, fiscal_code, phone, role, email, password) VALUES ('xiloID', 'xilo', 'xilo', null, null, null, 'trainer', 'trainer', :PWD);
INSERT INTO gym.users (id, name, surname, birth_date, fiscal_code, phone, role, email, password) VALUES ('ivanID', 'ivan', 'ivan', null, null, null, 'customer', 'customer', :PWD);
INSERT INTO gym.users (id, name, surname, birth_date, fiscal_code, phone, role, email, password) VALUES ('floID', 'flo', 'flo', null, null, null, 'manager', 'manager', :PWD);
INSERT INTO gym.users (id, name, surname, birth_date, fiscal_code, phone, role, email, password) VALUES ('adminID', 'admin', 'admin', null, null, null, 'admin', 'admin', :PWD);

INSERT INTO gym.rooms values ('1', 'weight_room');
INSERT INTO gym.rooms values ('2', 'cyber_robics');
INSERT INTO gym.rooms values ('3', 'cross_fit');

INSERT INTO gym.courses VALUES ('CyberRobicsCourseID', 'CyberRobics', 'You also have to be lifting heavy weights', 'xiloID');
INSERT INTO gym.courses VALUES ('CrossFitCourseID', 'CrossFit', 'You also have to do crossift', 'xiloID');

INSERT INTO gym.lessons VALUES (gen_random_uuid(), '2021-12-25', '8:00:00', 30, 'CyberRobicsCourseID');
INSERT INTO gym.lessons VALUES (gen_random_uuid(), '2021-12-23', '9:00:00', 20, 'CyberRobicsCourseID');
INSERT INTO gym.lessons VALUES (gen_random_uuid(), '2021-12-22', '10:00:00', 40, 'CrossFitCourseID');
INSERT INTO gym.lessons VALUES (gen_random_uuid(), '2021-12-19', '11:00:00', 50, 'CrossFitCourseID');
INSERT INTO gym.lessons VALUES (gen_random_uuid(), '2021-12-19', '12:00:00', 20, 'CrossFitCourseID');


INSERT INTO gym.subscriptions VALUES ('abbonamentoDiIvan', '2021-11-19', '2022-11-19', 2000.15, 'ivanID');
INSERT INTO gym.transactions VALUES (gen_random_uuid(), '2021-12-28', '16:00:00', 'acqua', 'abbonamentoDiIvan');
INSERT INTO gym.transactions VALUES (gen_random_uuid(), '2021-12-28', '17:00:00', 'felpa', 'abbonamentoDiIvan');
INSERT INTO gym.transactions VALUES (gen_random_uuid(), '2021-12-22', '19:00:00', 'proteine', 'abbonamentoDiIvan');


INSERT INTO gym.accesses VALUES (gen_random_uuid(), '2021-12-22', '19:00:00', '20:00:00', 'ivanID');
INSERT INTO gym.accesses VALUES (gen_random_uuid(), '2021-12-21', '19:00:00', '20:00:00', 'ivanID');
INSERT INTO gym.accesses VALUES (gen_random_uuid(), '2021-12-22', '19:00:00', '20:00:00', 'floID');
INSERT INTO gym.accesses VALUES (gen_random_uuid(), '2021-12-21', '19:00:00', '20:00:00', 'floID');
INSERT INTO gym.accesses VALUES (gen_random_uuid(), '2021-12-22', '19:00:00', '20:00:00', 'xiloID');
INSERT INTO gym.accesses VALUES (gen_random_uuid(), '2021-12-21', '19:00:00', '23:00:00', 'xiloID');
INSERT INTO gym.accesses VALUES (gen_random_uuid(), '2021-12-11', '19:00:00', '22:00:00', 'ivanID');
INSERT INTO gym.accesses VALUES (gen_random_uuid(), '2021-12-10', '19:00:00', '21:00:00', 'ivanID');
INSERT INTO gym.accesses VALUES (gen_random_uuid(), '2021-12-11', '19:00:00', '23:00:00', 'floID');
INSERT INTO gym.accesses VALUES (gen_random_uuid(), '2021-12-12', '19:00:00', '21:00:00', 'floID');
INSERT INTO gym.accesses VALUES (gen_random_uuid(), '2021-12-11', '19:00:00', '22:00:00', 'xiloID');
INSERT INTO gym.accesses VALUES (gen_random_uuid(), '2021-12-12', '19:00:00', '21:00:00', 'xiloID');