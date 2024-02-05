USE FLAGS;

CREATE TABLE flags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flag_value VARCHAR(255) NOT NULL
);

INSERT INTO flags (flag_value) VALUES
    ('Flag1'),
    ('Flag2'),
    ('Flag3'),
    ('Flag4'),
    ('Flag5'),
    ('Flag6'),
    ('Flag7'),
    ('Flag8'),
    ('Flag9'),
    ('test_flagXD');
