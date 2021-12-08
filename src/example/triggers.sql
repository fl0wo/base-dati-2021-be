--Controllo che la riga in Courses punti sempre a un trainer e mai a un user o admin
CREATE OR REPLACE FUNCTION "gym".is_trainer_fun() RETURNS trigger AS $$

DECLARE
    trainer_row "gym".users%ROWTYPE= NULL;

    BEGIN
        SELECT * INTO trainer_row
        FROM "gym".users u
        WHERE u.id=NEW.trainer;

        IF trainer_row.role == 'trainer' THEN
            RETURN NEW;
        ELSE
            RETURN NULL;
        END IF;
    END
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS is_trainer ON "gym".courses;
CREATE TRIGGER is_trainer
BEFORE INSERT OR UPDATE ON "gym".courses
FOR EACH ROW
EXECUTE FUNCTION "gym".is_trainer_fun();



--Controlla che le prenotazioni per sala pesi non siano al limite per un detterminato slot
CREATE OR REPLACE FUNCTION "gym".is_slot_full_fun() RETURNS trigger AS $$

DECLARE
    slot_row "gym".slots%ROWTYPE= NULL;
    current_occupation integer;

    BEGIN
        SELECT * INTO slot_row
        FROM "gym".slots slot
        WHERE slot.id=NEW.slot;

        SELECT COUNT(*) INTO current_occupation
        FROM "gym".weight_room_reservations wr
        WHERE wr.slot = NEW.slot;

        IF current_occupation>=slot_row.max_capacity THEN
        DELETE FROM "gym".reservations r
        WHERE r.id = NEW.reservation_id;
            RETURN NULL;
        ELSE
            RETURN NEW;
        END IF;
    END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS is_slot_full ON "gym".weight_room_reservations;
CREATE TRIGGER is_slot_full
BEFORE INSERT OR UPDATE ON "gym".weight_room_reservations
FOR EACH ROW
EXECUTE FUNCTION "gym".is_slot_full_fun();

--Controlla che le prenotazioni per le lezioni non siano al limite per una detterminata lezione
CREATE OR REPLACE FUNCTION "gym".is_lesson_full_fun() RETURNS trigger AS $$

DECLARE
    lesson_row "gym".lessons%ROWTYPE= NULL;
    current_occupation integer;

    BEGIN
        SELECT * INTO lesson_row
        FROM "gym".lessons lesson
        WHERE lesson.id=NEW.lesson;

        SELECT COUNT(*) INTO current_occupation
        FROM "gym".lesson_reservation lr
        WHERE lr.lesson = NEW.lesson;

        IF current_occupation+1>lesson_row.max_participants THEN
            DELETE FROM "gym".reservations r
            WHERE r.id = NEW.reservation_id;
            RETURN NULL;
        ELSE
            RETURN NEW;
        END IF;
    END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS is_lesson_full ON "gym".lesson_reservation;
CREATE TRIGGER is_lesson_full
BEFORE INSERT OR UPDATE ON "gym".lesson_reservation
FOR EACH ROW
EXECUTE FUNCTION "gym".is_lesson_full_fun();



-- Controlla che l'abbonamento sia valido quando si fa un accesso
CREATE OR REPLACE FUNCTION "gym".check_subscription()
RETURNS trigger AS $$

DECLARE
    subscription "gym".subscriptions%ROWTYPE=NULL;

BEGIN
    SELECT * INTO subscription
    FROM "gym".subscription s
    WHERE s.user = NEW.user;

    IF subscription.start_date < NOW() AND subscription.end_date > NOW() THEN
        RETURN NEW;
    ELSE
        RETURN NULL;
    END IF;
END
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS check_subscription ON "gym".accesses;
CREATE TRIGGER check_subscription
BEFORE INSERT OR UPDATE ON "gym".accesses
FOR EACH ROW
EXECUTE FUNCTION "gym".check_subscription();
