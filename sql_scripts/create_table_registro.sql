-- Table: public.registro

-- DROP TABLE IF EXISTS public.registro;

CREATE TABLE IF NOT EXISTS public.registro
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    doc_id integer NOT NULL,
    materia_id integer NOT NULL,
    partes text COLLATE pg_catalog."default" NOT NULL,
    n_processo text COLLATE pg_catalog."default" NOT NULL,
    data_atuacao date NOT NULL,
    url text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT registro_pkey PRIMARY KEY (id),
    CONSTRAINT n_processo UNIQUE (n_processo)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.registro
    OWNER to postgres;