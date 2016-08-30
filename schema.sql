drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    "story_title" text not null,
    "user_story" text not null,
    "acceptance_criteria" text not null,
    "business_value" integer not null,
    "estimation" decimal(3, 2) not null,
    "status" text not null
);