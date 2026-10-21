# Autofocus API differences: October 8052 OTA versus September 8054 stock

Read-only comparison of normalized JADX 1.5.6 method digests; proprietary Java code not published.
Identical method digests indicate identical normalized decompiled bodies; differences need semantic validation.

## Method comparison

- same: 15928
- changed: 10

## Hardware-related changed methods

- changed — com/hysd/ai/AiFileUtils.java :: CheckHysdFiles(boolean isForce)
- changed — com/hysd/ai/RuiCameraApi.java :: RuiCameraApi(android.content.Context context)
- changed — com/hysd/ai/RuiCameraApi.java :: startTof()
- changed — com/hysd/client/VAF2S.java :: onCreate()
- changed — com/hysd/client/VAF2S.java :: onStartCommand(android.content.Intent intent, int flags, int startId)
- changed — com/hysd/xymscreen/MainActivity.java :: onCreate(android.os.Bundle savedInstanceState)
- changed — com/hysd/xymscreen/MainActivity.java :: onReceive(android.content.Context context, android.content.Intent intent)
- changed — com/hysd/xymscreen/MainActivity.java :: onStart()
- changed — com/hysd/xymscreen/MainActivity.java :: updateDataFast()
- changed — com/hysd/xymscreen/MainActivity.java :: updateDataSlow()

## Limitations

- These are implementation-level indications, not evidence of different physical motor drivers.
- Method hashes can differ with compiler optimization, library packaging and decompiler changes.
- Never call unknown motor/ToF methods on real hardware without limits and stop/recovery controls.

