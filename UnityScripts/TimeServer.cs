using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TimeServer : MonoBehaviour
{
    long physics_time = 0;
    long frame_time = 0;
    
    [Tooltip("Use system time for timestamps rather than Unity time")]
    public bool realtime = false;
    long physics_frame_count = 0;

    DateTime sys_start;

    public long GetPhysicsTicks()
    {
        return physics_time;
    }

    public long GetFrameTicks()
    {
        return frame_time;
    }

    public long GetTimeNow()
    {   
        if (realtime) {
            return DateTime.UtcNow.Subtract(new DateTime(1970, 1, 1)).Ticks;
        } else {
            return Mathf.RoundToInt(Time.fixedDeltaTime * (float)1e7) * physics_frame_count;
        }
    }

    public long GetSimTime()
    {
        return GetTimeNow();
    }

    public long GetSysTime()
    {
        return DateTime.UtcNow.Subtract(new DateTime(1970, 1, 1)).Ticks;
    }

    public long GetSysTimeElapsed()
    {
        return DateTime.UtcNow.Subtract(sys_start).Ticks;
    }

    public float GetTimeNowFloat()
    {   
        return this.GetTimeNow() / 10000000.0f;
    }

    public float GetSysTimeElapsedFloat()
    {   
        return this.GetSysTimeElapsed() / 10000000.0f;
    }    

    void Start()
    {
        sys_start = DateTime.UtcNow;
    }

    void FixedUpdate()
    {
        physics_time = GetTimeNow();
        physics_frame_count++;
    }

    void Update()
    {
        frame_time = GetTimeNow();
    }
}
