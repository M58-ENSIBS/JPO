# Challenge JPO - ENSIBS

This directory contains the entire challeneg for the ENSIBS open days. 

The challenge was reserved for beginners in the field, with 7 flags of increasing difficulty (easy -> medium).
## Authors

- [@M58](https://www.github.com/M58-ENSIBS)
- Help from [@couttcoutt](https://github.com/coutand-bastien)
    and [@Alleph](https://github.com/Alleph)

## Deployment

To deploy this project, a docker-compose file is provided to run the challenge in a container. 

```bash
  docker-compose up -d
```
After that, the challenge is available on port 80 of the host machine.

Warning : In the docker-compose file, these lines : 
```
RUN apt-get update && apt-get install -y locales && locale-gen fr_FR.UTF-8
ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR:fr
ENV LC_ALL fr_FR.UTF-8
```
are used to set the locale to french. Otherwise the timsestamps in the logs are in english.


## Features

Throughout the challenge, the story evolves to set up a mini-scenario for the player. 

7 flags are hidden in a logical order :

```
CLOG{1st_ch4ll3ng3_1s_4lw4ys_3asy}
CLOG{2nd_flag_h1dd3n_1n_r4nd0m_pl4c3}
CLOG{3rd_flag_l4st_ea5y_0ne!!!}
CLOG{4th_V3rb_T4mpering_1N_A_NuTsh3ll}
CLOG{5th_Wh0_1s_3mpl0y33_0f_th3_y34r?}
CLOG{6th_Supr3m3_L34d3r_0f_jWt?}
CLOG{7th_Fr0m_Intern_To_Adm1n_of_Csssr_Webs1te?}
```

A `POC.py` file is provided to test the flags.
