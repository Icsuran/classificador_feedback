DROP DATABASE IF EXISTS allura;

CREATE DATABASE allura;

\c allura;

-- considerei id como pk. Logo, requisicoes com o mesmo id terao erro

CREATE TABLE feedbacks (
    id uuid,
    feedback text,
    sentiment character varying(100) check (sentiment in('POSITIVO','NEGATIVO','INCONCLUSIVO')),
    code character varying(100),
    reason text,    
    data_created timestamp default current_timestamp,
    primary key (id)
);

