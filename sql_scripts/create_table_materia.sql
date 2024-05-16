-- Table: public.materia

-- DROP TABLE IF EXISTS public.materia;

CREATE TABLE IF NOT EXISTS public.materia
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    materia text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT materia_pkey PRIMARY KEY (id),
    CONSTRAINT materia_materia_key UNIQUE (materia)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.materia
    OWNER to postgres;