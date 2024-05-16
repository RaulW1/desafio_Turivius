-- Table: public.doc

-- DROP TABLE IF EXISTS public.doc;

CREATE TABLE IF NOT EXISTS public.doc
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    doc text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT doc_pkey PRIMARY KEY (id),
    CONSTRAINT constraint_name UNIQUE (doc)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.doc
    OWNER to postgres;