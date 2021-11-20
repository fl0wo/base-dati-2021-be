
--Controllo che la riga in Courses punti sempre a un trainer e mai a un user o admin
CREATE OR REPLACE FUNCTION "gym".is_trainer_fun() RETURNS trigger AS $$

DECLARE
    trainer_row "gym".users%ROWTYPE= NULL;

    BEGIN
        SELECT * INTO trainer_row
        FROM "gym".users u
        WHERE u.id=NEW.trainer;

        IF trainer_row.role=='trainer' THEN
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
    --   TODO: use rollback instead
    --    DELETE FROM "gym".reservations r
    --    WHERE r.id = NEW.reservation_id;
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
        FROM "gym".lesson_reservations lr
        WHERE lr.lesson = NEW.lesson;

        IF current_occupation+1>lesson_row.max_partecipants THEN
            DELETE FROM "gym".reservations r
            WHERE r.id = NEW.reservation_id;
            RETURN NULL;
        ELSE
            RETURN NEW;
        END IF;
    END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS is_lesson_full ON "gym".lesson_reservations;
CREATE TRIGGER is_lesson_full
BEFORE INSERT OR UPDATE ON "gym".lesson_reservations
FOR EACH ROW
EXECUTE FUNCTION "gym".is_lesson_full_fun()



-- Controlla che l'utente abbia iscrizione valida e abbia abbastanza soldi per compare prodotto //IVAN
CREATE OR REPLACE FUNCTION "gym".check_transaction()
RETURNS trigger AS $$

DECLARE
    product "gym".products%ROWTYPE=NULL;
    subscription "gym".subscriptions%ROWTYPE=NULL;

BEGIN
    SELECT * INTO product
    FROM "gym".products p
    WHERE p.id = NEW.product;

    SELECT * INTO subscription
    FROM "gym".subscriptions s
    WHERE s.id = NEW.subscription;

    IF subscription.end_date > current_date AND product.price <= subscription.cur_balance THEN
        RETURN NEW;
    ELSE
        RETURN NULL;
    END IF;
END;

DROP TRIGGER IF EXISTS check_transaction ON "gym".transactions
CREATE TRIGGER check_transaction
BEFORE INSERT OR UPDATE ON "gym".transactions
FOR EACH ROW
EXECUTE FUNCTION "gym".check_transaction


-- Controlla che l'iscrizione non sia fatta da Admin o Istrtuttori //IVAN
CREATE OR REPLACE FUNCTION "gym".check_subscription()
RETURNS trigger AS $$

DECLARE
    client "gym".users%ROWTYPE=NULL;

BEGIN
    SELECT * INTO client
    FROM "gym".users u
    WHERE u.id = NEW.user

    IF client.role <> "User" THEN
        RETURN NULL
    ELSE
        RETURN NEW
    END IF;
END

DROP TRIGGER IF EXISTS check_transaction ON "gym".subscription
CREATE TRIGGER check_subscription
BEFORE INSERT OR UPDATE ON "gym".subscription
FOR EACH ROW
EXECUTE FUNCTION "gym".subscription

$$ LANGUAGE plpgsql;
