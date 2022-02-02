CREATE TABLE "users" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "email" CHAR NOT NULL,
  "password" VARCHAR(45) NOT NULL,
  "created" timestamp NOT NULL,
  "is_active" BOOLEAN NOT NULL,
  "is_superuser" BOOLEAN NOT NULL,
  "is_staff" BOOLEAN NOT NULL,
  "accept_private_policy" BOOLEAN NOT NULL,
  "name" VARCHAR,
  "surname" VARCHAR,
  "patronymic" VARCHAR,
  "birthday" date
);

CREATE TABLE "requests_logs" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "request_user" INTEGER NOT NULL,
  "pacient" INTEGER NOT NULL,
  "table_name" VARCHAR NOT NULL,
  "table_row" INTEGER NOT NULL
);

CREATE TABLE "pacients" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "user" INTEGER NOT NULL,
  "phone" VARCHAR(45) UNIQUE NOT NULL
);

CREATE TABLE "doctors" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "phone" VARCHAR(45) UNIQUE NOT NULL,
  "user" INTEGER NOT NULL
);

CREATE TABLE "chat_room" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "pacient" INTEGER NOT NULL,
  "doctor" INTEGER NOT NULL
);

CREATE TABLE "chat_message" (
  "id" INTEGER NOT NULL,
  "chat_room" INTEGER NOT NULL,
  "pacient" INTEGER,
  "doctor" INTEGER,
  "created" timestamp NOT NULL,
  "delivered" BOOLEAN,
  "read" BOOLEAN,
  PRIMARY KEY ("id", "chat_room")
);

CREATE TABLE "medicine_card" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "user" INTEGER UNIQUE NOT NULL,
  "height" float,
  "weight" float,
  "average_pressure" VARCHAR
);

CREATE TABLE "pressure_results" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "medicine_card" INTEGER NOT NULL,
  "datetime" timestamp,
  "result" VARCHAR
);

CREATE TABLE "sugar_level" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "medicine_card" INTEGER NOT NULL,
  "datetime" timestamp,
  "result" VARCHAR
);

CREATE TABLE "transferred_diseases" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "medicine_card" INTEGER NOT NULL,
  "disease" INTEGER NOT NULL,
  "diagnosis" VARCHAR,
  "diagnosis_date" date,
  "diagnosis_year" INTEGER,
  "treatment_date" date,
  "treatment_end_date" date
);

CREATE TABLE "diseases" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "title" VARCHAR UNIQUE NOT NULL,
  "code" VARCHAR
);

CREATE TABLE "through_diseases_analyzes" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "disease" INTEGER,
  "analysis" INTEGER
);

CREATE TABLE "chronic_diseases" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "medicine_card" INTEGER NOT NULL,
  "disease" INTEGER NOT NULL,
  "treatment" TEXT
);

CREATE TABLE "transferred_operations" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "medicine_card" INTEGER NOT NULL,
  "operation" INTEGER NOT NULL,
  "operation_datetime" timestamp,
  "effect" VARCHAR
);

CREATE TABLE "discharge_epicrisis" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "disease" INTEGER
);

CREATE TABLE "discharge_epicrisis_files" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "discharge_epicris" INTEGER
);

CREATE TABLE "operations" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "title" VARCHAR UNIQUE NOT NULL
);

CREATE TABLE "analysis_results" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "pacient" INTEGER NOT NULL,
  "medicine_card" INTEGER NOT NULL,
  "analysis" INTEGER NOT NULL,
  "result" TEXT,
  "date_" date
);

CREATE TABLE "analysis_results_images" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "imagefile" VARCHAR,
  "analysis_results" INTEGER NOT NULL
);

CREATE TABLE "analysis_results_files" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "file" VARCHAR,
  "analysis_results" INTEGER NOT NULL
);

CREATE TABLE "appointment_order" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "pacient" INTEGER NOT NULL,
  "doctor" INTEGER NOT NULL,
  "datetime" timestamp NOT NULL,
  "confirmation" BOOLEAN NOT NULL,
  "created" timestamp NOT NULL,
  "appointment_took_place" BOOLEAN NOT NULL,
  "doctor_subspecialization" INTEGER,
  "doctor_specialization" INTEGER NOT NULL,
  "hospital" INTEGER NOT NULL
);

CREATE TABLE "survey" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "complaints" TEXT,
  "complaints_date" date,
  "treatment" TEXT,
  "appointment_order" INTEGER
);

CREATE TABLE "doctors_appointment" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "pacient" INTEGER NOT NULL,
  "doctor" INTEGER NOT NULL,
  "appointment_order" INTEGER,
  "anamnesis" TEXT NOT NULL,
  "datetime" timestamp NOT NULL,
  "medicine_card" INTEGER NOT NULL,
  "doctor_specialization" INTEGER NOT NULL,
  "doctor_subspecialization" INTEGER,
  "complaints" TEXT,
  "complaints_date" date,
  "treatment" TEXT,
  "rating_for_pacient" INTEGER,
  "rating_for_doctor" INTEGER
);

CREATE TABLE "prescription_of_medicines" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "medicine_card" INTEGER NOT NULL,
  "doctors_appointnent" INTEGER NOT NULL,
  "medicine" INTEGER NOT NULL,
  "duration" INTEGER NOT NULL,
  "rate" INTEGER NOT NULL,
  "number" INTEGER NOT NULL,
  "per" VARCHAR
);

CREATE TABLE "medicines" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "title" VARCHAR NOT NULL
);

CREATE TABLE "prescription_of_procedures" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "medicine_card" INTEGER NOT NULL,
  "doctors_appointment" INTEGER NOT NULL,
  "procedure" INTEGER NOT NULL,
  "duration" INTEGER NOT NULL,
  "rate" INTEGER NOT NULL,
  "number" INTEGER NOT NULL,
  "per" VARCHAR
);

CREATE TABLE "procedures" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "title" VARCHAR NOT NULL
);

CREATE TABLE "prescription_of_analyzes" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "medicine_card" INTEGER NOT NULL,
  "doctors_appointnent" INTEGER NOT NULL,
  "analysis" INTEGER NOT NULL
);

CREATE TABLE "analyzes" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "title" VARCHAR NOT NULL
);

CREATE TABLE "doctors_specialization" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "title" VARCHAR(45) UNIQUE NOT NULL
);

CREATE TABLE "doctors_supspecialization" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "doctor_specialization" INTEGER NOT NULL,
  "title" VARCHAR(45) UNIQUE NOT NULL
);

CREATE TABLE "through_doctor_subspec" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "doctor" INTEGER NOT NULL,
  "doctor_subspecialization" INTEGER NOT NULL
);

CREATE TABLE "through_doctors_specialization" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "doctor" INTEGER NOT NULL,
  "specialization" INTEGER NOT NULL
);

CREATE TABLE "hospitals" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "title" VARCHAR(45) NOT NULL,
  "town" VARCHAR(45) NOT NULL,
  "address" VARCHAR(45) NOT NULL
);

CREATE TABLE "through_doctors_hospitals" (
  "id" INTEGER PRIMARY KEY NOT NULL,
  "doctor" INTEGER NOT NULL,
  "hospital" INTEGER NOT NULL
);

ALTER TABLE "pacients" ADD FOREIGN KEY ("user") REFERENCES "users" ("id");

ALTER TABLE "doctors" ADD FOREIGN KEY ("user") REFERENCES "users" ("id");

ALTER TABLE "medicine_card" ADD FOREIGN KEY ("user") REFERENCES "pacients" ("id");

ALTER TABLE "appointment_order" ADD FOREIGN KEY ("pacient") REFERENCES "pacients" ("id");

ALTER TABLE "appointment_order" ADD FOREIGN KEY ("doctor") REFERENCES "doctors" ("id");

ALTER TABLE "appointment_order" ADD FOREIGN KEY ("doctor_subspecialization") REFERENCES "doctors_supspecialization" ("id");

ALTER TABLE "appointment_order" ADD FOREIGN KEY ("doctor_specialization") REFERENCES "doctors_specialization" ("id");

ALTER TABLE "appointment_order" ADD FOREIGN KEY ("hospital") REFERENCES "hospitals" ("id");

ALTER TABLE "doctors_appointment" ADD FOREIGN KEY ("pacient") REFERENCES "pacients" ("id");

ALTER TABLE "doctors_appointment" ADD FOREIGN KEY ("doctor") REFERENCES "doctors" ("id");

ALTER TABLE "doctors_appointment" ADD FOREIGN KEY ("appointment_order") REFERENCES "appointment_order" ("id");

ALTER TABLE "doctors_appointment" ADD FOREIGN KEY ("medicine_card") REFERENCES "medicine_card" ("id");

ALTER TABLE "doctors_appointment" ADD FOREIGN KEY ("doctor_specialization") REFERENCES "doctors_specialization" ("id");

ALTER TABLE "doctors_appointment" ADD FOREIGN KEY ("doctor_subspecialization") REFERENCES "doctors_supspecialization" ("id");

ALTER TABLE "prescription_of_medicines" ADD FOREIGN KEY ("medicine_card") REFERENCES "medicine_card" ("id");

ALTER TABLE "prescription_of_medicines" ADD FOREIGN KEY ("doctors_appointnent") REFERENCES "doctors_appointment" ("id");

ALTER TABLE "prescription_of_analyzes" ADD FOREIGN KEY ("id") REFERENCES "doctors_appointment" ("id");

ALTER TABLE "prescription_of_analyzes" ADD FOREIGN KEY ("id") REFERENCES "medicine_card" ("id");

ALTER TABLE "prescription_of_medicines" ADD FOREIGN KEY ("medicine") REFERENCES "medicines" ("id");

ALTER TABLE "prescription_of_procedures" ADD FOREIGN KEY ("procedure") REFERENCES "procedures" ("id");

ALTER TABLE "prescription_of_analyzes" ADD FOREIGN KEY ("analysis") REFERENCES "analyzes" ("id");

ALTER TABLE "prescription_of_procedures" ADD FOREIGN KEY ("medicine_card") REFERENCES "medicine_card" ("id");

ALTER TABLE "prescription_of_procedures" ADD FOREIGN KEY ("doctors_appointment") REFERENCES "doctors_appointment" ("id");

ALTER TABLE "doctors_supspecialization" ADD FOREIGN KEY ("doctor_specialization") REFERENCES "doctors_specialization" ("id");

ALTER TABLE "through_doctor_subspec" ADD FOREIGN KEY ("doctor") REFERENCES "doctors" ("id");

ALTER TABLE "through_doctor_subspec" ADD FOREIGN KEY ("doctor_subspecialization") REFERENCES "doctors_supspecialization" ("id");

ALTER TABLE "through_doctors_specialization" ADD FOREIGN KEY ("doctor") REFERENCES "doctors" ("id");

ALTER TABLE "through_doctors_specialization" ADD FOREIGN KEY ("specialization") REFERENCES "doctors_specialization" ("id");

ALTER TABLE "analysis_results" ADD FOREIGN KEY ("medicine_card") REFERENCES "medicine_card" ("id");

ALTER TABLE "analysis_results" ADD FOREIGN KEY ("analysis") REFERENCES "analyzes" ("id");

ALTER TABLE "analysis_results" ADD FOREIGN KEY ("pacient") REFERENCES "pacients" ("id");

ALTER TABLE "analysis_results_images" ADD FOREIGN KEY ("analysis_results") REFERENCES "analysis_results" ("id");

ALTER TABLE "requests_logs" ADD FOREIGN KEY ("request_user") REFERENCES "users" ("id");

ALTER TABLE "requests_logs" ADD FOREIGN KEY ("pacient") REFERENCES "pacients" ("id");

ALTER TABLE "chat_room" ADD FOREIGN KEY ("pacient") REFERENCES "pacients" ("id");

ALTER TABLE "chat_room" ADD FOREIGN KEY ("doctor") REFERENCES "doctors" ("id");

ALTER TABLE "chat_room" ADD FOREIGN KEY ("id") REFERENCES "chat_message" ("chat_room");

ALTER TABLE "chat_message" ADD FOREIGN KEY ("pacient") REFERENCES "pacients" ("id");

ALTER TABLE "chat_message" ADD FOREIGN KEY ("doctor") REFERENCES "doctors" ("id");

ALTER TABLE "analysis_results_files" ADD FOREIGN KEY ("id") REFERENCES "analysis_results" ("id");

ALTER TABLE "transferred_diseases" ADD FOREIGN KEY ("medicine_card") REFERENCES "medicine_card" ("id");

ALTER TABLE "transferred_operations" ADD FOREIGN KEY ("medicine_card") REFERENCES "medicine_card" ("id");

ALTER TABLE "transferred_operations" ADD FOREIGN KEY ("operation") REFERENCES "operations" ("id");

ALTER TABLE "transferred_diseases" ADD FOREIGN KEY ("disease") REFERENCES "diseases" ("id");

ALTER TABLE "pressure_results" ADD FOREIGN KEY ("medicine_card") REFERENCES "medicine_card" ("id");

ALTER TABLE "sugar_level" ADD FOREIGN KEY ("medicine_card") REFERENCES "medicine_card" ("id");

ALTER TABLE "through_doctors_hospitals" ADD FOREIGN KEY ("hospital") REFERENCES "hospitals" ("id");

ALTER TABLE "through_doctors_hospitals" ADD FOREIGN KEY ("doctor") REFERENCES "doctors" ("id");

ALTER TABLE "chronic_diseases" ADD FOREIGN KEY ("medicine_card") REFERENCES "medicine_card" ("id");

ALTER TABLE "chronic_diseases" ADD FOREIGN KEY ("disease") REFERENCES "diseases" ("id");

ALTER TABLE "discharge_epicrisis" ADD FOREIGN KEY ("disease") REFERENCES "chronic_diseases" ("id");

ALTER TABLE "discharge_epicrisis" ADD FOREIGN KEY ("disease") REFERENCES "transferred_diseases" ("id");

ALTER TABLE "discharge_epicrisis_files" ADD FOREIGN KEY ("discharge_epicris") REFERENCES "discharge_epicrisis" ("id");

ALTER TABLE "through_diseases_analyzes" ADD FOREIGN KEY ("disease") REFERENCES "diseases" ("id");

ALTER TABLE "through_diseases_analyzes" ADD FOREIGN KEY ("analysis") REFERENCES "analyzes" ("id");

ALTER TABLE "appointment_order" ADD FOREIGN KEY ("id") REFERENCES "survey" ("appointment_order");

