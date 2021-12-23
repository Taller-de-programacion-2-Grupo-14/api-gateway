create table courses(
    name varchar(255) not null,
    id serial not null,
    exams int not null,
    creator_id int not null,
    type varchar(255) not null,
    subscription varchar(255) not null,
    description varchar(1500) not null,
    hashtags varchar(1000) default (''),
    location varchar(255) not null,
    cancelled int default (0),
    created_at timestamp default (now()),
    updated_at timestamp default (now()),
    blocked boolean default (false),
    pile_pic_url varchar(1000) default (''),
    primary key(id),
    unique (name, creator_id)
);

create table enrolled(
    id_course int not null,
    id_student int not null,
    status varchar(255) default 'on course' check (status in ('on course', 'approved', 'failed')),
    foreign key(id_course) references courses(id) on delete cascade,
    primary key(id_course, id_student)
);

create table collaborators(
    id_collaborator int not null,
    id_course int not null,
    foreign key(id_course) references courses(id) on delete cascade,
    primary key(id_course, id_collaborator)
);

create table favoriteCourses(
    course_id int not null,
    user_id int not null,
    foreign key (course_id) references courses(id) on delete cascade,
    primary key (course_id, user_id)
);

create table multimedia(
    course_id int not null,
    title varchar(255) default (''),
    tag varchar(255) default (''),
    url varchar(1000) not null,
    created_at timestamp default (now()),
    updated_at timestamp default (now()),
    foreign key (course_id) references courses(id) on delete cascade,
    primary key (course_id, url)
);

CREATE TABLE user_registry
(
    id       SERIAL,
    email    varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (email)
);

CREATE INDEX emailIndex
    ON user_registry (email);

CREATE TABLE profile_user
(
    user_id    int          NOT NULL,
    email      varchar(255),
    first_name varchar(100) NOT NULL,
    last_name  varchar(100) NOT NULL,
    interest   varchar(255),
    photo_url   varchar(255),
    location   varchar(255),
    subscription varchar(255) default 'free' check (subscription in ('free', 'platinum', 'black')),
    is_admin boolean default false,
    blocked boolean default false,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES user_registry (id) ON DELETE CASCADE,
    UNIQUE (email)
);

CREATE INDEX emailIndexProfile
    ON profile_user (email);

CREATE TABLE user_tokens (
                             user_id int NOT NULL,
                             token varchar(1000) default NULL,
                             created_at timestamp default now(),
                             primary key (user_id),
                             FOREIGN KEY (user_id) REFERENCES user_registry (id)
);

CREATE TABLE waiting_update (
                                user_id int not null,
                                new_subscription varchar(255) default 'free' check (new_subscription in ('free', 'platinum', 'black')),
                                txn_hash varchar(255),
                                primary key (user_id, new_subscription),
                                foreign key (user_id) references user_registry
);

