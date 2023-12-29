CREATE TABLE articles (
  articleName varchar NOT NULL,
  articleUrl varchar NOT NULL,
  linkTime date NOT NULL,
  PRIMARY KEY (articleName, articleUrl)
);