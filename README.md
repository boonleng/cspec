Cell Spectral Analysis
===

This is a collection of notebooks in the processing of developing the Adaptive Spectrum Processing technique for wind-turbine contamination mitigation.

There are two newly modules:
- `cspec` - Cell spectral analysis
- `toshi` - Toshiba data reader for I/Q data

There are two demo notebooks:
 - Demo 01 - Using `toshi` module
 - Demo 02 - Adaptive Spectrum Processing

There are five development notebooks:
 - Dev 01 - Reading IQ Data
 - Dev 02 - Read Functions
 - Dev 03 - Geographic and Cartesian Coordinates
 - Dev 04 - Coordinate Array Transformation
 - Dev 05 - Preview

The two demo notebooks represent most of usable components in this project. The development notebooks are mainly for development and experimentation only. They may not fully function on other machines.

2021
===
Datasets to process:

- 01/28 12:40
- 08/09 17:00
- 07/28 18:00
- 02/01 10:15
- 08/14 15:30
- 08/09 09:00
- 07/28 04:00
- 08/09 01:00
- 01/15 10:20
- 01/15 10:38

Turbine locations:
1, 5.333, 354.32
2, 5.307, 351.26
3, 5.606, 350.12
4, 5.874, 350.89
5, 6.108, 350.06
6, 6.749, 348.95
7, 6.976, 348.99
8, 11.799, 342.54
9, 12.073, 342.17
10, 12.347, 341.90
11, 12.609, 341.43
12, 12.895, 340.91
13, 13.160, 340.53
14, 13.421, 340.01
15, 13.722, 339.60
16, 13.992, 339.25
17, 14.265, 338.81
18, 14.528, 338.45
19, 14.794, 338.06
20, 15.057, 337.67
21, 15.316, 337.29
22, 15.573, 336.92
23, 15.846, 336.64
24, 16.136, 336.64
25, 5.531, 170.60
26, 5.170, 170.44
27, 5.591, 167.29

Random Notes
===
HD2
└── akita
    ├── IQ
    │   ├── IQdata
    │   │   ├── 2020.06.14
    │   │   │   ├── 15
    │   │   │   ├── 16
    │   │   │   ├── 17
    │   │   │   ├── 18
    │   │   │   ├── 19
    │   │   │   ├── 20
    │   │   │   ├── 21
    │   │   │   ├── 22
    │   │   │   └── 23
    │   │   ├── 2020.06.15
    │   │   │   ├── 00
    │   │   │   ├── 01
    │   │   │   ├── 02
    │   │   │   ├── 22
    │   │   │   └── 23
    │   │   └── 2020.06.16
    │   │       ├── 00
    │   │       ├── 01
    │   │       ├── 02
    │   │       ├── 03
    │   │       ├── 04
    │   │       ├── 05
    │   │       ├── 06
    │   │       ├── 07
    │   │       └── 08
    │   └── IQpara
    │       ├── 2020.06.14
    │       │   ├── 15
    │       │   ├── 16
    │       │   ├── 17
    │       │   ├── 18
    │       │   ├── 19
    │       │   ├── 20
    │       │   ├── 21
    │       │   ├── 22
    │       │   └── 23
    │       ├── 2020.06.15
    │       │   ├── 00
    │       │   ├── 01
    │       │   ├── 02
    │       │   ├── 22
    │       │   └── 23
    │       └── 2020.06.16
    │           ├── 00
    │           ├── 01
    │           ├── 02
    │           ├── 03
    │           ├── 04
    │           ├── 05
    │           ├── 06
    │           ├── 07
    │           └── 08
    └── RAW
        └── RAWdata
            ├── 2020.06.14
            │   ├── 15
            │   ├── 16
            │   ├── 17
            │   ├── 18
            │   ├── 19
            │   ├── 20
            │   ├── 21
            │   ├── 22
            │   └── 23
            ├── 2020.06.15
            │   ├── 00
            │   ├── 01
            │   ├── 02
            │   ├── 22
            │   └── 23
            └── 2020.06.16
                ├── 00
                ├── 01
                ├── 02
                ├── 03
                ├── 04
                ├── 05
                ├── 06
                ├── 07
                └── 08

