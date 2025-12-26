
CREATE TABLE IF NOT EXISTS "activity_types" (
	"id" serial NOT NULL UNIQUE,
	"type_name" varchar(255) NOT NULL,
	PRIMARY KEY("id")
);

CREATE INDEX "activity_types_index_0"
ON "activity_types" ("type_name");
CREATE TABLE IF NOT EXISTS "fitness_data" (
	"id" serial NOT NULL UNIQUE,
	"recorded_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	"activity_type_id" int NOT NULL,
	"steps" int NOT NULL,
	"distance_km" float NOT NULL,
	"kilocalories" float NOT NULL,
	"lat" float NOT NULL,
	"lon" float NOT NULL,
	PRIMARY KEY("id")
);


ALTER TABLE "fitness_data"
ADD FOREIGN KEY("activity_type_id") REFERENCES "activity_types"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;