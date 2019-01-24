CREATE TABLE IF NOT EXISTS users(
    id serial PRIMARY KEY,
    firstname varchar(25) NOT NULL,
    lastname varchar(25) NOT NULL,
    othername varchar(25),
    email varchar(50) NOT NULL UNIQUE,
    phonenumber varchar(12) NOT NULL UNIQUE,
    username varchar(12) NOT NULL UNIQUE,
    password varchar(250) NOT NULL,
    isadmin BOOLEAN NOT NULL,
    registered TIMESTAMP DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS incidents(
    id serial NOT NULL PRIMARY KEY,
    createdon TIMESTAMP DEFAULT NOW(),
    title varchar(255) NOT NULL UNIQUE,
    createdby INT NOT NULL,
    type varchar(25), 
    location varchar(50) NOT NULL,
    status varchar(12) NOT NULL,
    comment varchar(12) NOT NULL UNIQUE,
    updatedby INT,
    FOREIGN KEY (createdby) REFERENCES users (id)
    ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS incidents_images(
    owner INT NOT NULL,
    filename CHARACTER VARYING(255) NOT NULL,
    mime_type CHARACTER VARYING(255) NOT NULL,
    file_data BYTEA NOT NULL, 
    FOREIGN KEY (owner) REFERENCES incidents(id)
    ON UPDATE CASCADE ON DELETE CASCADE
);