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

=> sort by time

- 2020/07/28 04:00
- 2020/07/28 18:00
- 2020/08/09 01:00
- 2020/08/09 09:00
- 2020/08/09 17:00
- 2020/08/14 15:30
- 2021/01/15 10:20
- 2021/01/15 10:38
- 2021/01/28 12:40
- 2021/02/01 10:15


Random Notes
===

```
└── IQdata
    ├── 2020.07.28
    │   ├── 04
    │   │   ├── 20200728_040012.511494-05-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200728_040030.337918-06-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200728_040048.017743-07-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200728_040105.594534-08-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200728_040123.170043-09-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200728_040140.858967-0A-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200728_040158.642915-0B-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200728_040216.527845-0C-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200728_040234.101494-0D-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200728_040251.670607-0E-9B.iqData.XXXX.AKITA.dat
    │   │   └── 20200728_040309.344374-0F-9B.iqData.XXXX.AKITA.dat
    │   └── 18
    │       ├── 20200728_180003.697131-2B-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200728_180021.274630-2C-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200728_180039.151327-2D-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200728_180056.726433-2E-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200728_180114.597952-2F-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200728_180132.173258-30-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200728_180149.745119-31-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200728_180207.427280-32-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200728_180225.006322-33-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200728_180242.583929-34-9B.iqData.XXXX.AKITA.dat
    │       └── 20200728_180300.160136-35-9B.iqData.XXXX.AKITA.dat
    ├── 2020.08.09
    │   ├── 01
    │   │   ├── 20200809_010015.710512-0F-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200809_010033.287429-10-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200809_010050.871760-11-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200809_010108.449326-12-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200809_010126.134122-13-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200809_010143.722705-14-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200809_010201.325691-15-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200809_010219.119773-16-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200809_010236.700115-17-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200809_010254.376683-18-9B.iqData.XXXX.AKITA.dat
    │   │   └── 20200809_010311.956195-19-9B.iqData.XXXX.AKITA.dat
    │   ├── 09
    │   │   ├── 20200809_090012.087545-6E-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200809_090029.658910-6F-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200809_090047.233363-70-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200809_090104.909088-71-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200809_090122.481867-72-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200809_090140.059969-73-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200809_090157.733226-74-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200809_090215.306122-75-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200809_090232.980761-76-9B.iqData.XXXX.AKITA.dat
    │   │   ├── 20200809_090250.561456-77-9B.iqData.XXXX.AKITA.dat
    │   │   └── 20200809_090308.133507-78-9B.iqData.XXXX.AKITA.dat
    │   └── 17
    │       ├── 20200809_170006.112787-CD-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200809_170023.786954-CE-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200809_170041.560431-CF-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200809_170059.232871-D0-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200809_170117.009646-D1-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200809_170134.682286-D2-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200809_170152.257463-D3-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200809_170209.829279-D4-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200809_170227.409353-D5-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200809_170245.084221-D6-9B.iqData.XXXX.AKITA.dat
    │       └── 20200809_170302.657709-D7-9B.iqData.XXXX.AKITA.dat
    ├── 2020.08.14
    │   └── 15
    │       ├── 20200814_153014.804652-33-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200814_153032.382007-34-9B.iqData.XXXX.AKITA.dat
    │       ├── 20200814_153049.959797-35-9B.iqData.XXXX.AKITA.dat
    │       └── 20200814_153107.537321-36-9B.iqData.XXXX.AKITA.dat
    ├── 2021.01.15
    │   └── 10
    │       ├── 20210115_102022.845024-3F-1D.iqData.XXXX.AKITA.dat
    │       ├── 20210115_102116.951752-3F-1D.iqData.XXXX.AKITA.dat
    │       ├── 20210115_103733.065083-3F-20.iqData.XXXX.AKITA.dat
    │       ├── 20210115_103827.178452-3F-20.iqData.XXXX.AKITA.dat
    │       └── 20210115_103921.272146-3F-20.iqData.XXXX.AKITA.dat
    ├── 2021.01.28
    │   └── 12
    │       ├── 20210128_124008.095007-CA-68.iqData.XXXX.AKITA.dat
    │       ├── 20210128_124025.640488-CB-68.iqData.XXXX.AKITA.dat
    │       ├── 20210128_124043.250859-CC-68.iqData.XXXX.AKITA.dat
    │       └── 20210128_124100.876775-CD-68.iqData.XXXX.AKITA.dat
    └── 2021.02.01
        └── 10
            ├── 20210201_101004.804248-46-68.iqData.XXXX.AKITA.dat
            ├── 20210201_101504.800791-57-68.iqData.XXXX.AKITA.dat
            ├── 20210201_101522.464873-58-68.iqData.XXXX.AKITA.dat
            ├── 20210201_101540.032327-59-68.iqData.XXXX.AKITA.dat
            └── 20210201_101557.653728-5A-68.iqData.XXXX.AKITA.dat
```