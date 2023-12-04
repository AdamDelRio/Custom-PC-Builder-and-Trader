
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

CREATE EXTENSION IF NOT EXISTS "pgsodium" WITH SCHEMA "pgsodium";

CREATE EXTENSION IF NOT EXISTS "pg_graphql" WITH SCHEMA "graphql";

CREATE EXTENSION IF NOT EXISTS "pg_stat_statements" WITH SCHEMA "extensions";

CREATE EXTENSION IF NOT EXISTS "pgcrypto" WITH SCHEMA "extensions";

CREATE EXTENSION IF NOT EXISTS "pgjwt" WITH SCHEMA "extensions";

CREATE EXTENSION IF NOT EXISTS "supabase_vault" WITH SCHEMA "vault";

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA "extensions";

SET default_tablespace = '';

SET default_table_access_method = "heap";

CREATE TABLE IF NOT EXISTS "public"."cart_items" (
    "cart_id" integer NOT NULL,
    "part_id" integer NOT NULL,
    "quantity" integer NOT NULL,
    "id" integer NOT NULL,
    "user_item" boolean NOT NULL,
    "checked_out" boolean DEFAULT false NOT NULL,
    CONSTRAINT "cart_items_quantity_check" CHECK (("quantity" > 0))
);

ALTER TABLE "public"."cart_items" OWNER TO "postgres";

ALTER TABLE "public"."cart_items" ALTER COLUMN "cart_id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."cart_items_cart_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

ALTER TABLE "public"."cart_items" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."cart_items_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."carts" (
    "cart_id" integer NOT NULL,
    "user_id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT ("now"() AT TIME ZONE 'utc'::"text") NOT NULL
);

ALTER TABLE "public"."carts" OWNER TO "postgres";

ALTER TABLE "public"."carts" ALTER COLUMN "cart_id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."cart_table_cart_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."case_specs" (
    "id" integer NOT NULL,
    "part_id" bigint NOT NULL,
    "name" "text" NOT NULL,
    "type" "text",
    "color" "text",
    "psu" "text",
    "side_panel" "text",
    "external_volume" numeric,
    "internal_35_bays" integer
);

ALTER TABLE "public"."case_specs" OWNER TO "postgres";

ALTER TABLE "public"."case_specs" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."case_specs_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."cpu_specs" (
    "id" integer NOT NULL,
    "part_id" bigint NOT NULL,
    "name" "text" NOT NULL,
    "core_count" integer,
    "core_clock" numeric,
    "boost_clock" numeric,
    "tdp" integer,
    "graphics" "text",
    "smt" boolean
);

ALTER TABLE "public"."cpu_specs" OWNER TO "postgres";

ALTER TABLE "public"."cpu_specs" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."cpu_specs_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."customers" (
    "id" integer NOT NULL,
    "name" "text" NOT NULL,
    "address" "text" NOT NULL,
    "phone" "text" NOT NULL,
    "user_id" bigint NOT NULL
);

ALTER TABLE "public"."customers" OWNER TO "postgres";

CREATE TABLE IF NOT EXISTS "public"."video_card_specs" (
    "id" integer NOT NULL,
    "part_id" bigint NOT NULL,
    "name" "text" NOT NULL,
    "chipset" "text",
    "memory" integer,
    "core_clock" integer,
    "boost_clock" integer,
    "color" "text",
    "length" integer
);

ALTER TABLE "public"."video_card_specs" OWNER TO "postgres";

ALTER TABLE "public"."video_card_specs" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."gpu_specs_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."internal_hard_drive_specs" (
    "id" integer NOT NULL,
    "part_id" bigint NOT NULL,
    "name" "text" NOT NULL,
    "capacity" integer,
    "price_per_gb" integer,
    "type" "text",
    "cache" integer,
    "form_factor" "text",
    "interface" "text"
);

ALTER TABLE "public"."internal_hard_drive_specs" OWNER TO "postgres";

CREATE TABLE IF NOT EXISTS "public"."monitor_specs" (
    "id" integer NOT NULL,
    "part_id" bigint NOT NULL,
    "name" "text" NOT NULL,
    "screen_size" numeric,
    "resolution" "text",
    "refresh_rate" integer,
    "response_time" real,
    "panel_type" "text",
    "aspect_ratio" "text"
);

ALTER TABLE "public"."monitor_specs" OWNER TO "postgres";

ALTER TABLE "public"."monitor_specs" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."monitor_specs_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."motherboard_specs" (
    "id" integer NOT NULL,
    "part_id" bigint NOT NULL,
    "name" "text" NOT NULL,
    "socket" "text",
    "form_factor" "text",
    "max_memory" integer,
    "memory_slots" integer,
    "color" "text"
);

ALTER TABLE "public"."motherboard_specs" OWNER TO "postgres";

ALTER TABLE "public"."motherboard_specs" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."motherboard_specs_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."part_inventory" (
    "part_id" integer NOT NULL,
    "name" "text" NOT NULL,
    "type" "text" NOT NULL,
    "quantity" integer NOT NULL,
    "dollars" integer DEFAULT 0 NOT NULL,
    "cents" integer DEFAULT 0 NOT NULL,
    "id" integer NOT NULL,
    CONSTRAINT "part_inventory_quantity_check" CHECK (("quantity" >= 0))
);

ALTER TABLE "public"."part_inventory" OWNER TO "postgres";

ALTER TABLE "public"."part_inventory" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."part_inventory_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

ALTER TABLE "public"."part_inventory" ALTER COLUMN "part_id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."part_inventory_part_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."pc_template_parts" (
    "id" integer NOT NULL,
    "template_id" bigint NOT NULL,
    "user_id" bigint NOT NULL,
    "part_id" bigint NOT NULL,
    "quantity" integer NOT NULL,
    "created_at" timestamp with time zone DEFAULT ("now"() AT TIME ZONE 'utc'::"text") NOT NULL,
    "user_part" boolean DEFAULT false NOT NULL
);

ALTER TABLE "public"."pc_template_parts" OWNER TO "postgres";

ALTER TABLE "public"."pc_template_parts" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."pc_template_parts_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."pc_templates" (
    "id" integer NOT NULL,
    "user_id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT ("now"() AT TIME ZONE 'utc'::"text") NOT NULL
);

ALTER TABLE "public"."pc_templates" OWNER TO "postgres";

ALTER TABLE "public"."pc_templates" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."pc_template_table_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."power_supply_specs" (
    "id" integer NOT NULL,
    "part_id" bigint NOT NULL,
    "name" "text" NOT NULL,
    "type" "text",
    "efficiency" "text",
    "wattage" integer,
    "modular" "text",
    "color" "text"
);

ALTER TABLE "public"."power_supply_specs" OWNER TO "postgres";

ALTER TABLE "public"."power_supply_specs" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."power_supply_specs_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."purchase_history" (
    "id" integer NOT NULL,
    "user_id" integer NOT NULL,
    "created_at" timestamp with time zone DEFAULT ("now"() AT TIME ZONE 'utc'::"text") NOT NULL,
    "part_id" integer NOT NULL,
    "user_item" boolean DEFAULT false NOT NULL,
    "dollars" integer DEFAULT 1 NOT NULL,
    "cents" integer DEFAULT 0 NOT NULL,
    CONSTRAINT "purchase_history_cents_check" CHECK (("cents" >= 0)),
    CONSTRAINT "purchase_history_dollars_check" CHECK (("dollars" >= 0))
);

ALTER TABLE "public"."purchase_history" OWNER TO "postgres";

ALTER TABLE "public"."purchase_history" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."purchase_history_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

ALTER TABLE "public"."internal_hard_drive_specs" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."storage_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."user_parts" (
    "id" integer NOT NULL,
    "user_id" bigint NOT NULL,
    "part_id" bigint NOT NULL,
    "quantity" integer DEFAULT 0 NOT NULL,
    "dollars" integer DEFAULT 0 NOT NULL,
    "cents" integer DEFAULT 0 NOT NULL,
    CONSTRAINT "user_parts_quantity_check" CHECK (("quantity" >= 0))
);

ALTER TABLE "public"."user_parts" OWNER TO "postgres";

ALTER TABLE "public"."user_parts" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."user_parts_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."users" (
    "id" integer NOT NULL,
    "username" "text" NOT NULL,
    "email" "text" NOT NULL
);

ALTER TABLE "public"."users" OWNER TO "postgres";

ALTER TABLE "public"."customers" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."users_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

ALTER TABLE "public"."users" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."users_id_seq1"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

ALTER TABLE ONLY "public"."cart_items"
    ADD CONSTRAINT "cart_items_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."carts"
    ADD CONSTRAINT "cart_table_pkey" PRIMARY KEY ("cart_id");

ALTER TABLE ONLY "public"."case_specs"
    ADD CONSTRAINT "case_specs_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."cpu_specs"
    ADD CONSTRAINT "cpu_specs_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."video_card_specs"
    ADD CONSTRAINT "gpu_specs_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."monitor_specs"
    ADD CONSTRAINT "monitor_specs_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."motherboard_specs"
    ADD CONSTRAINT "motherboard_specs_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."part_inventory"
    ADD CONSTRAINT "part_inventory_id_key" UNIQUE ("id");

ALTER TABLE ONLY "public"."part_inventory"
    ADD CONSTRAINT "part_inventory_pkey" PRIMARY KEY ("part_id");

ALTER TABLE ONLY "public"."pc_template_parts"
    ADD CONSTRAINT "pc_template_parts_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."pc_templates"
    ADD CONSTRAINT "pc_template_table_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."power_supply_specs"
    ADD CONSTRAINT "power_supply_specs_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."purchase_history"
    ADD CONSTRAINT "purchase_history_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."internal_hard_drive_specs"
    ADD CONSTRAINT "storage_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."user_parts"
    ADD CONSTRAINT "user_parts_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."users"
    ADD CONSTRAINT "users_email_key" UNIQUE ("email");

ALTER TABLE ONLY "public"."customers"
    ADD CONSTRAINT "users_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."users"
    ADD CONSTRAINT "users_pkey1" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."users"
    ADD CONSTRAINT "users_username_key" UNIQUE ("username");

ALTER TABLE ONLY "public"."cart_items"
    ADD CONSTRAINT "cart_items_cart_id_fkey" FOREIGN KEY ("cart_id") REFERENCES "public"."carts"("cart_id");

ALTER TABLE ONLY "public"."cart_items"
    ADD CONSTRAINT "cart_items_part_id_fkey" FOREIGN KEY ("part_id") REFERENCES "public"."part_inventory"("part_id");

ALTER TABLE ONLY "public"."case_specs"
    ADD CONSTRAINT "case_specs_part_id_fkey" FOREIGN KEY ("part_id") REFERENCES "public"."part_inventory"("part_id") ON UPDATE CASCADE;

ALTER TABLE ONLY "public"."customers"
    ADD CONSTRAINT "customers_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id");

ALTER TABLE ONLY "public"."internal_hard_drive_specs"
    ADD CONSTRAINT "internal_hard_drive_specs_part_id_fkey" FOREIGN KEY ("part_id") REFERENCES "public"."part_inventory"("part_id") ON UPDATE CASCADE;

ALTER TABLE ONLY "public"."monitor_specs"
    ADD CONSTRAINT "monitor_specs_part_id_fkey" FOREIGN KEY ("part_id") REFERENCES "public"."part_inventory"("part_id") ON DELETE CASCADE;

ALTER TABLE ONLY "public"."motherboard_specs"
    ADD CONSTRAINT "motherboard_specs_part_id_fkey" FOREIGN KEY ("part_id") REFERENCES "public"."part_inventory"("part_id") ON DELETE CASCADE;

ALTER TABLE ONLY "public"."pc_template_parts"
    ADD CONSTRAINT "pc_template_parts_part_id_fkey" FOREIGN KEY ("part_id") REFERENCES "public"."part_inventory"("part_id");

ALTER TABLE ONLY "public"."pc_template_parts"
    ADD CONSTRAINT "pc_template_parts_template_id_fkey" FOREIGN KEY ("template_id") REFERENCES "public"."pc_templates"("id");

ALTER TABLE ONLY "public"."pc_template_parts"
    ADD CONSTRAINT "pc_template_parts_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id");

ALTER TABLE ONLY "public"."pc_templates"
    ADD CONSTRAINT "pc_templates_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id");

ALTER TABLE ONLY "public"."power_supply_specs"
    ADD CONSTRAINT "power_supply_specs_part_id_fkey" FOREIGN KEY ("part_id") REFERENCES "public"."part_inventory"("part_id") ON UPDATE CASCADE;

ALTER TABLE ONLY "public"."user_parts"
    ADD CONSTRAINT "user_parts_part_id_fkey" FOREIGN KEY ("part_id") REFERENCES "public"."part_inventory"("part_id") ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY "public"."user_parts"
    ADD CONSTRAINT "user_parts_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY "public"."video_card_specs"
    ADD CONSTRAINT "video_card_specs_part_id_fkey" FOREIGN KEY ("part_id") REFERENCES "public"."part_inventory"("part_id") ON UPDATE CASCADE;

ALTER TABLE "public"."cart_items" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."carts" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."case_specs" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."cpu_specs" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."customers" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."internal_hard_drive_specs" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."monitor_specs" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."motherboard_specs" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."part_inventory" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."pc_template_parts" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."pc_templates" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."power_supply_specs" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."purchase_history" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."user_parts" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."users" ENABLE ROW LEVEL SECURITY;

ALTER TABLE "public"."video_card_specs" ENABLE ROW LEVEL SECURITY;

GRANT USAGE ON SCHEMA "public" TO "postgres";
GRANT USAGE ON SCHEMA "public" TO "anon";
GRANT USAGE ON SCHEMA "public" TO "authenticated";
GRANT USAGE ON SCHEMA "public" TO "service_role";

GRANT ALL ON TABLE "public"."cart_items" TO "anon";
GRANT ALL ON TABLE "public"."cart_items" TO "authenticated";
GRANT ALL ON TABLE "public"."cart_items" TO "service_role";

GRANT ALL ON SEQUENCE "public"."cart_items_cart_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."cart_items_cart_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."cart_items_cart_id_seq" TO "service_role";

GRANT ALL ON SEQUENCE "public"."cart_items_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."cart_items_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."cart_items_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."carts" TO "anon";
GRANT ALL ON TABLE "public"."carts" TO "authenticated";
GRANT ALL ON TABLE "public"."carts" TO "service_role";

GRANT ALL ON SEQUENCE "public"."cart_table_cart_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."cart_table_cart_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."cart_table_cart_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."case_specs" TO "anon";
GRANT ALL ON TABLE "public"."case_specs" TO "authenticated";
GRANT ALL ON TABLE "public"."case_specs" TO "service_role";

GRANT ALL ON SEQUENCE "public"."case_specs_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."case_specs_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."case_specs_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."cpu_specs" TO "anon";
GRANT ALL ON TABLE "public"."cpu_specs" TO "authenticated";
GRANT ALL ON TABLE "public"."cpu_specs" TO "service_role";

GRANT ALL ON SEQUENCE "public"."cpu_specs_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."cpu_specs_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."cpu_specs_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."customers" TO "anon";
GRANT ALL ON TABLE "public"."customers" TO "authenticated";
GRANT ALL ON TABLE "public"."customers" TO "service_role";

GRANT ALL ON TABLE "public"."video_card_specs" TO "anon";
GRANT ALL ON TABLE "public"."video_card_specs" TO "authenticated";
GRANT ALL ON TABLE "public"."video_card_specs" TO "service_role";

GRANT ALL ON SEQUENCE "public"."gpu_specs_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."gpu_specs_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."gpu_specs_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."internal_hard_drive_specs" TO "anon";
GRANT ALL ON TABLE "public"."internal_hard_drive_specs" TO "authenticated";
GRANT ALL ON TABLE "public"."internal_hard_drive_specs" TO "service_role";

GRANT ALL ON TABLE "public"."monitor_specs" TO "anon";
GRANT ALL ON TABLE "public"."monitor_specs" TO "authenticated";
GRANT ALL ON TABLE "public"."monitor_specs" TO "service_role";

GRANT ALL ON SEQUENCE "public"."monitor_specs_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."monitor_specs_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."monitor_specs_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."motherboard_specs" TO "anon";
GRANT ALL ON TABLE "public"."motherboard_specs" TO "authenticated";
GRANT ALL ON TABLE "public"."motherboard_specs" TO "service_role";

GRANT ALL ON SEQUENCE "public"."motherboard_specs_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."motherboard_specs_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."motherboard_specs_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."part_inventory" TO "anon";
GRANT ALL ON TABLE "public"."part_inventory" TO "authenticated";
GRANT ALL ON TABLE "public"."part_inventory" TO "service_role";

GRANT ALL ON SEQUENCE "public"."part_inventory_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."part_inventory_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."part_inventory_id_seq" TO "service_role";

GRANT ALL ON SEQUENCE "public"."part_inventory_part_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."part_inventory_part_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."part_inventory_part_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."pc_template_parts" TO "anon";
GRANT ALL ON TABLE "public"."pc_template_parts" TO "authenticated";
GRANT ALL ON TABLE "public"."pc_template_parts" TO "service_role";

GRANT ALL ON SEQUENCE "public"."pc_template_parts_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."pc_template_parts_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."pc_template_parts_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."pc_templates" TO "anon";
GRANT ALL ON TABLE "public"."pc_templates" TO "authenticated";
GRANT ALL ON TABLE "public"."pc_templates" TO "service_role";

GRANT ALL ON SEQUENCE "public"."pc_template_table_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."pc_template_table_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."pc_template_table_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."power_supply_specs" TO "anon";
GRANT ALL ON TABLE "public"."power_supply_specs" TO "authenticated";
GRANT ALL ON TABLE "public"."power_supply_specs" TO "service_role";

GRANT ALL ON SEQUENCE "public"."power_supply_specs_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."power_supply_specs_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."power_supply_specs_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."purchase_history" TO "anon";
GRANT ALL ON TABLE "public"."purchase_history" TO "authenticated";
GRANT ALL ON TABLE "public"."purchase_history" TO "service_role";

GRANT ALL ON SEQUENCE "public"."purchase_history_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."purchase_history_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."purchase_history_id_seq" TO "service_role";

GRANT ALL ON SEQUENCE "public"."storage_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."storage_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."storage_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."user_parts" TO "anon";
GRANT ALL ON TABLE "public"."user_parts" TO "authenticated";
GRANT ALL ON TABLE "public"."user_parts" TO "service_role";

GRANT ALL ON SEQUENCE "public"."user_parts_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."user_parts_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."user_parts_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."users" TO "anon";
GRANT ALL ON TABLE "public"."users" TO "authenticated";
GRANT ALL ON TABLE "public"."users" TO "service_role";

GRANT ALL ON SEQUENCE "public"."users_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."users_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."users_id_seq" TO "service_role";

GRANT ALL ON SEQUENCE "public"."users_id_seq1" TO "anon";
GRANT ALL ON SEQUENCE "public"."users_id_seq1" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."users_id_seq1" TO "service_role";

ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "service_role";

ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "service_role";

ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "service_role";

RESET ALL;