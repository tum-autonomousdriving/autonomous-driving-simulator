English | [中文](https://github.com/tum-autonomousdriving/.github/blob/main/profile/README_zh.md)
# Autonomous Driving System

<p align="center"> <img alt="GitHub release" src="https://github.com/tum-autonomousdriving/.github/blob/main/images/Logo.png", width = "400"></p>

## Contents

- [Introduction](#introduction)
- [Framework](#framework)
- [Functions](#functions)
- [Members](#members)

## Introduction

The large-scale application of fully autonomous driving technology is the key to solving traffic congestion and reducing traffic accidents, and it is also an effective way to deal with the shortage of human resources. Commercial fully autonomous driving technology is expected to be deployed in the next five to ten years. However, this technology is currently only in the hands of a very small number of top technology companies. The vast majority of traditional automakers are not good at this technology, although they are eager to obtain this technology. We are developing a fully autonomous driving system that can be shared with traditional automakers, thereby accelerating the large-scale application of fully autonomous driving technology.

At present, our product is an autonomous driving system that can run in a simulation environment. We developed this simulator and trained autonomous driving algorithms such as environment perception, global/local path planning and decision making based on this simulator. Although this system works well in the simulator, it still needs road tests to verify its performance in the real environment, and then conduct large-scale simulation tests, repeating the cycle, and finally form a safe, reliable and practical autonomous driving system.
## Framework
![image](https://github.com/tum-autonomousdriving/.github/blob/main/images/framework.png)

## Functions
* ### High-definition digital twins of real cities and roads
Simulate complex and changeable real road scenarios to improve the ability of autonomous driving algorithms to deal with such scenarios.
<table>
  <tr>
    <td vlign="center">
      <img src="https://github.com/tum-autonomousdriving/.github/blob/main/images/urban.png" alt="Pin popup window">
    </td>
    <td vlign="center">
      <img src="https://github.com/tum-autonomousdriving/.github/blob/main/images/urban2.png" alt="Popup window">
    </td>
  </tr>
</table>

* ### Simulation of light and weather changes
Simulate changes in light and weather to improve the robustness of autonomous driving algorithms.
<table>
  <tr>
    <td vlign="center">
      <img src="https://github.com/tum-autonomousdriving/.github/blob/main/images/light.png" alt="Pin popup window", width ="600">
    </td>
    <td vlign="center">
      <img src="https://github.com/tum-autonomousdriving/.github/blob/main/images/weather.png" alt="Popup window", width ="600">
    </td>
  </tr>
</table>

* ### Automatic Data Labeling
The automatic data annotation function can automatically generate labels for training 2D/3D object detection and semantic/instance segmentation algorithms.
<table>
  <tr>
    <td vlign="center">
      <img src="https://github.com/tum-autonomousdriving/.github/blob/main/images/lable.png" alt="Pin popup window">
    </td>
    <td vlign="center">
      <img src="https://github.com/tum-autonomousdriving/.github/blob/main/images/segmentation.png" alt="Popup window">
    </td>
  </tr>
</table>

* ### Industrial LiDAR Simulation
Integrated Unity industrial-grade lidar simulation for training and testing 3D object detection, distance estimation and SLAM algorithms.
<table>
  <tr>
    <td vlign="center">
      <img src="https://github.com/tum-autonomousdriving/.github/blob/main/images/sim1.png" alt="Pin popup window", width ="600">
    </td>
    <td vlign="center">
      <img src="https://github.com/tum-autonomousdriving/.github/blob/main/images/Sim2.jpg" alt="Popup window", width ="600">
    </td>
  </tr>
</table>


## Members

<a href="https://www.ce.cit.tum.de/air/home/">Chair of Robotics, Artificial Intelligence and Real-time Systems, Technical University of Munich</a>

### Supervisor

* **[Prof. Dr.-Ing. habil. Alois Christian Knoll](https://www.ce.cit.tum.de/air/people/prof-dr-ing-habil-alois-knoll/)**

### Programmers
* **[Zhou Liguo](https://www.ce.cit.tum.de/air/people/liguo-zhou/)**, *M.Sc.* - Project Coordinator
* **Dipl.-Ing. Cao Wei**, *M.Sc.*
* **Liu Hongshen**
* **Ma Liang**
* **[Liu Hao](linkedin.com/in/hao-liu97)**
* **Song Yinglei**
* **Li Haichuan**
* **Cui Chuanlu**
* **Liu Yang**
* **Gao Yichao**

### Artist
* **Liu Lian**

### External Members
* Zhang Jingyu; Zhang Hanzhen, *M.Sc.*; Meng Jun
* Zhang Chao, *M.Sc.*; Lin Tianhao, *M.Sc.*; Wang Ruining; Huo Yifan; Ren Peng; Zhang Yujie
