# OEM settings and hardware interfaces — RUIOS 8052 latest OTA

Read-only static study of SHA256-verified OTA 8052 Oct 2026 (one HDMI).
App signatures extracted via JADX. JNI dynamic symbols collected with readelf.
No proprietary decompiled Java source is committed.
No code has been executed on a real projector. Interfaces remain unverified at runtime.

## APK inventory

| App | Package | Classes | JNI libraries | Selected privileged permissions |
|---|---|---:|---|---|
| TvSettingsPlus | com.android.tv.settings | 5796 | com_mediatek_net_jni, com_mediatek_twoworlds_tv_jni, settingsi2c_jni | android.permission.BLUETOOTH, android.permission.BLUETOOTH_ADMIN, android.permission.BLUETOOTH_ADVERTISE, android.permission.BLUETOOTH_CONNECT, android.permission.BLUETOOTH_PRIVILEGED, android.permission.BLUETOOTH_SCAN |
| Factory | mediatek.factorymenu.ui | 1866 | com_mediatek_net_jni, com_mediatek_twoworlds_tv_jni, factoryi2c_jni | android.permission.BLUETOOTH, android.permission.BLUETOOTH_ADMIN |
| RuiAutoFocus | com.hysd.screen | 1091 | com_mediatek_twoworlds_tv_jni, focusvahysd, ruicameraapi_jni | android.permission.INTERACT_ACROSS_USERS |
| KeystoneCorrection | com.rjpj.tcorrection | 449 | i2c_jni | — |
| KuSourceRJ | com.coolux.source | 3007 | — | — |
| trdmiddle | com.trd.framework | 568 | com_mediatek_twoworlds_tv_jni, tof_jni, trd_jni, trdmiddle | android.permission.BLUETOOTH_CONNECT |
| trdservice | com.trd.service | 438 | rjpj_private_function | android.permission.BLUETOOTH_CONNECT, android.permission.HDMI_CEC |
| KuSettings | com.my.settings | 3470 | — | android.permission.BLUETOOTH, android.permission.BLUETOOTH_ADMIN, android.permission.BLUETOOTH_CONNECT, android.permission.BLUETOOTH_PRIVILEGED, android.permission.BLUETOOTH_SCAN, android.permission.MANAGE_ACCOUNTS |

## Settings I2C and hardware — TvSettingsPlus

- No matching declaration surfaced; inspect the structured JSON.

Call-site identifiers (without proprietary Java body):

- com/android/tv/settings/uicustom/util/ProjectorManager.java line 32: setProjectorMirrorMode
- com/android/tv/settings/uicustom/util/ProjectorManager.java line 43: i2c
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java line 331: resetTrapezoid
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java line 528: resetTrapezoid
- com/android/tv/settings/uicustom/floatmenu/controller/projector/ProjectionModeSecondaryController.java line 121: setProjectorMirrorMode
- com/android/tv/settings/uicustom/floatmenu/controller/projector/ProjectionModeSecondaryController.java line 131: setProjectorMirrorMode
- com/android/tv/settings/uicustom/floatmenu/controller/projector/ProjectionModeSecondaryController.java line 141: setProjectorMirrorMode
- com/android/tv/settings/uicustom/floatmenu/controller/projector/ProjectionModeSecondaryController.java line 151: setProjectorMirrorMode

Referenced intent actions (strings only):

- android.bluetooth.device.action.PAIRING_REQUEST
- android.intent.action.VIEW
- com.rjpj.intent.action.auto.adjust.backlight.start
- com.rjpj.intent.action.auto.adjust.backlight.stop
- rjpj.action.manager.FILE

## Factory engineering interface — Factory

- mediatek/tvsetting/factory/ui/ProjectorManager.java :: i2c(false)
- mediatek/tvsetting/factory/ui/ProjectorManager.java :: i2c(false)
- mediatek/tvsetting/factory/ui/ProjectorManager.java :: i2c(true)
- mediatek/tvsetting/factory/ui/ProjectorManager.java :: i2c(true)
- mediatek/tvsetting/factory/ui/ProjectorManager.java :: if (i2CDevice != null)
- mediatek/tvsetting/factory/ui/ProjectorManager.java :: if (i2CDevice == null)
- mediatek/tvsetting/factory/ui/ProjectorManager.java :: if (i2CDevice2.open("/dev/i2c-1", com.mediatek.twoworlds.tv.MtkTvScanDvbsBase.DVBS_OPERATOR_NAME_CANAL_DIGITAL_SWE) == 0)
- mediatek/tvsetting/factory/ui/ProjectorManager.java :: private ProjectorManager()
- mediatek/tvsetting/factory/ui/ProjectorManager.java :: private void i2c(boolean z) throws java.lang.Throwable
- mediatek/tvsetting/factory/ui/ProjectorManager.java :: public int getProjectorMirrorMode()
- mediatek/tvsetting/factory/ui/ProjectorManager.java :: public static mediatek.tvsetting.factory.ui.ProjectorManager getInstance()
- mediatek/tvsetting/factory/ui/ProjectorManager.java :: public void setProjectorMirrorMode(android.content.Context context, int i) throws java.lang.Throwable
- mediatek/tvsetting/factory/ui/ProjectorManager.java :: synchronized (mediatek.tvsetting.factory.ui.ProjectorManager.class)
- mediatek/util/I2CDevice.java :: public native int open(java.lang.String str, int i) [native]
- mediatek/util/I2CDevice.java :: public native int readRegister(int i) [native]
- mediatek/util/I2CDevice.java :: public native int writeRegister(int i, int i2) [native]
- mediatek/util/I2CDevice.java :: public native void close() [native]

Call-site identifiers (without proprietary Java body):

- mediatek/tvsetting/factory/ui/ProjectorManager.java line 33: setProjectorMirrorMode
- mediatek/tvsetting/factory/ui/ProjectorManager.java line 39: i2c
- mediatek/tvsetting/factory/ui/ProjectorManager.java line 45: i2c
- mediatek/tvsetting/factory/ui/ProjectorManager.java line 51: i2c
- mediatek/tvsetting/factory/ui/ProjectorManager.java line 58: i2c
- mediatek/tvsetting/factory/ui/ProjectorManager.java line 70: i2c

Referenced intent actions (strings only):

- com.mediatek.select.source

## Focus motor, camera and ToF — RuiAutoFocus

- com/hysd/ai/RuiCameraApi.java :: if (com.hysd.ai.RuiCameraApi.this.mAccIndex >= 10)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI != null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI != null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI != null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI != null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI != null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI != null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI != null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI == null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI == null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI == null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI == null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI == null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI == null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI == null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI == null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI == null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI == null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI == null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI == null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI == null)
- com/hysd/ai/RuiCameraApi.java :: if (motorJNI == null)
- com/hysd/ai/RuiCameraApi.java :: private int getTofLDiffIntByString(java.lang.String str)
- com/hysd/ai/RuiCameraApi.java :: private int getTofRDiffIntByString(java.lang.String str)
- com/hysd/ai/RuiCameraApi.java :: public RuiCameraApi(android.content.Context context)
- com/hysd/ai/RuiCameraApi.java :: public int GetSensorCurMotorReturnCnt()
- com/hysd/ai/RuiCameraApi.java :: public int MotorBack()
- com/hysd/ai/RuiCameraApi.java :: public int MotorBackStep(int setRunStep)
- com/hysd/ai/RuiCameraApi.java :: public int MotorBackTofStep(int i, boolean z, int i2)
- com/hysd/ai/RuiCameraApi.java :: public int MotorFront()
- com/hysd/ai/RuiCameraApi.java :: public int MotorFrontStep(int setRunStep)
- com/hysd/ai/RuiCameraApi.java :: public int MotorFrontTofStep(int i, boolean z, int i2)
- com/hysd/ai/RuiCameraApi.java :: public int MotorStop()
- com/hysd/ai/RuiCameraApi.java :: public int SetSensorCurMotorReturnCnt(int step)
- com/hysd/ai/RuiCameraApi.java :: public int Trapezoid4Point(int[] data)
- com/hysd/ai/RuiCameraApi.java :: public int getProjectorMode()
- com/hysd/ai/RuiCameraApi.java :: public int getProjectorZoom()
- com/hysd/ai/RuiCameraApi.java :: public java.lang.String getRuiCameraApiEnv(java.lang.String strEnv)
- com/hysd/ai/RuiCameraApi.java :: public synchronized int getTofIcExist()
- com/hysd/ai/RuiCameraApi.java :: public synchronized int startTof()
- com/hysd/ai/RuiCameraApi.java :: public void AutoFocusFinish()
- com/hysd/ai/RuiCameraApi.java :: public void RuiCameraApiDestroy()
- com/hysd/ai/RuiCameraApi.java :: public void setProjectorMode(int mode)
- com/hysd/ai/RuiCameraApi.java :: public void setProjectorZoom(int zoom)
- com/hysd/ai/RuiCameraApi.java :: public void setRuiCameraApiEnv(java.lang.String strEnv, java.lang.String strValue)
- com/hysd/ai/RuiCameraApi.java :: setRuiCameraApiEnv(env, java.lang.String.valueOf(envVal))
- com/hysd/ai/RuiCameraApi.java :: setSysProp(PROP_SENSOR_ANGLE_FOCUS, "0")
- com/hysd/ai/RuiCameraApi.java :: synchronized (com.hysd.ai.RuiCameraApi.this.mAccLock)
- com/hysd/ai/RuiCameraApi.java :: throw new UnsupportedOperationException("Method not decompiled: com.hysd.ai.RuiCameraApi.GetAngle():float[]")
- com/hysd/client/HYSDkeystone.java :: delay(this.apis.get_motorslow())
- com/hysd/client/HYSDkeystone.java :: if (com.hysd.client.HYSDkeystone.this.apis.get_motordirection() == 1)
- com/hysd/client/HYSDkeystone.java :: if (com.hysd.client.HYSDkeystone.this.apis.get_motorstate() == 1)
- com/hysd/client/HYSDkeystone.java :: if (com.hysd.vafocus.HYSDVAF2.s0cam(this.camid, 2) == 1)
- com/hysd/client/HYSDkeystone.java :: if (this.apis.get_motor_type() == 0)
- com/hysd/client/HYSDkeystone.java :: if (this.apis.get_motor_type() == 0)
- com/hysd/client/HYSDkeystone.java :: if (this.apis.get_motor_type() == 0)
- com/hysd/client/HYSDkeystone.java :: if (this.apis.get_motor_type() == 0)
- com/hysd/client/HYSDkeystone.java :: if (this.apis.get_motordirection() == 1)
- com/hysd/client/HYSDkeystone.java :: if (this.apis.get_motorstate() == 1)
- com/hysd/client/HYSDkeystone.java :: motorbegin()
- com/hysd/client/HYSDkeystone.java :: public void KeyStoneRun3tof(final float[] tofdata, final int tofstate)
- com/hysd/client/HYSDkeystone.java :: public void quickKeyStoneRun3(int dmode, float[] tofdata, int tofstate, float a0, float a1, float a2, int reso)
- com/hysd/client/HYSDkeystone.java :: public void start_motor_thread_dvpcamera()
- com/hysd/client/HYSDkeystone.java :: public void toftest(int dmode, float[] tofdata, int tofstate, float a0, float a1, float a2, int reso)
- com/hysd/client/HYSDkeystone.java :: void motor_thread_run()
- com/hysd/client/HYSDkeystone.java :: while (com.hysd.client.HYSDkeystone.this.apis.get_motorrun())
- com/hysd/client/HYSDkeystone.java :: while (this.apis.get_motorrun())
- com/hysd/client/MotorAPIs2.java :: boolean get_motorrun()
- com/hysd/client/MotorAPIs2.java :: int get_motor_type()
- com/hysd/client/MotorAPIs2.java :: int get_motordirection()
- com/hysd/client/MotorAPIs2.java :: int get_motorslow()
- com/hysd/client/MotorAPIs2.java :: int get_motorstate()
- com/hysd/client/MotorAPIs2.java :: int getmotor_status()
- com/hysd/client/MotorAPIs2.java :: int getmotor_status2()
- com/hysd/client/MotorAPIs2.java :: int motor_back()
- com/hysd/client/MotorAPIs2.java :: int motor_forward()
- com/hysd/client/MotorAPIs2.java :: int motor_stop()
- com/hysd/client/MotorAPIs2.java :: int motorthread(int i)
- com/hysd/client/MotorAPIs2.java :: int motorthreadstop(int i)
- com/hysd/client/MotorAPIs2.java :: int setkeystone(int i, int i2, int i3, int i4, int i5, int i6, int i7, int i8)
- com/hysd/vafocus/HYSDVAF2.java :: public native byte[] gcamver(int i) [native]
- com/hysd/vafocus/HYSDVAF2.java :: public native double[] getsavedemmcdata() [native]
- com/hysd/vafocus/HYSDVAF2.java :: public native float[] afkeystone(com.hysd.client.MotorAPIs2 motorAPIs2, java.lang.String str, java.lang.String str2, int i, int i2, int i3, int i4, int i5, int i6, int i7, int i8, int i9, byte[] bArr, int i10, int i11, int i12, int i13) [native]
- com/hysd/vafocus/HYSDVAF2.java :: public native float[] afkeystone2(com.hysd.client.MotorAPIs2 motorAPIs2, java.lang.String str, java.lang.String str2, int i, int i2, int i3, int i4, int i5, int i6, byte[] bArr, int i7, int i8, int i9, int i10) [native]
- com/hysd/vafocus/HYSDVAF2.java :: public native float[] afkeystone3(com.hysd.client.MotorAPIs2 motorAPIs2, java.lang.String str, int i, int i2, int i3, int i4, int i5, int i6, int i7, byte[] bArr, int i8, int i9, int i10) [native]
- com/hysd/vafocus/HYSDVAF2.java :: public native float[] afkeystone3tof(com.hysd.client.MotorAPIs2 motorAPIs2, java.lang.String str, java.lang.String str2, int i, int i2, int i3, int i4, int i5, int i6, byte[] bArr, int i7, int i8, float[] fArr, int i9, int i10, int i11) [native]
- com/hysd/vafocus/HYSDVAF2.java :: public native float[] afkeystone3tofmcam(com.hysd.client.MotorAPIs2 motorAPIs2, java.lang.String str, int i, int i2, int i3, int i4, int i5, int i6, byte[] bArr, int i7, byte[] bArr2, int i8, float[] fArr, int i9, int i10, int i11) [native]
- com/hysd/vafocus/HYSDVAF2.java :: public native float[] calibtof(java.lang.String str, int i, float f, float f2) [native]
- com/hysd/vafocus/HYSDVAF2.java :: public native float[] getkeypoint(java.lang.String str) [native]
- com/hysd/vafocus/HYSDVAF2.java :: public native float[] gettofdata() [native]
- com/hysd/vafocus/HYSDVAF2.java :: public native float[] keystone2tof(java.lang.String str, float f, float f2) [native]
- com/hysd/vafocus/HYSDVAF2.java :: public native float[] quickkeystone(com.hysd.client.MotorAPIs2 motorAPIs2, java.lang.String str, java.lang.String str2, int i, int i2, int i3, int i4, int i5, int i6) [native]
- com/hysd/vafocus/HYSDVAF2.java :: public native float[] quickkeystone2(com.hysd.client.MotorAPIs2 motorAPIs2, java.lang.String str, java.lang.String str2, int i, int i2, int i3, int i4, float f, float f2, float f3, int i5, int i6) [native]
- com/hysd/vafocus/HYSDVAF2.java :: public native float[] quickkeystone2plus(com.hysd.client.MotorAPIs2 motorAPIs2, java.lang.String str, java.lang.String str2, int i, int i2, int i3, int i4, float f, float f2, float f3, int i5, int i6) [native]
- com/hysd/vafocus/HYSDVAF2.java :: public native float[] quickkeystone3(com.hysd.client.MotorAPIs2 motorAPIs2, java.lang.String str, java.lang.String str2, int i, int i2, int i3, int i4, float f, float f2, float f3, float[] fArr, int i5, int i6, int i7) [native]
- com/hysd/vafocus/HYSDVAF2.java :: public native float[] sfk(com.hysd.client.MotorAPIs2 motorAPIs2, java.lang.String str, java.lang.String str2, int i, int i2, int i3) [native]
- com/hysd/vafocus/HYSDVAF2.java :: public native int checkemmcdata(double[] dArr) [native]
- com/hysd/vafocus/HYSDVAF2.java :: public native int saveangle(java.lang.String str, float f, float f2) [native]
- com/hysd/vafocus/HYSDVAF2.java :: public native int savekeypoint(java.lang.String str, float[] fArr, int i, int i2, int i3) [native]
- com/hysd/vafocus/HYSDVAF2.java :: public native int setmac(java.lang.String str) [native]

Call-site identifiers (without proprietary Java body):

- com/hysd/ai/RuiCameraApi.java line 426: MotorFront
- com/hysd/ai/RuiCameraApi.java line 435: MotorBack
- com/hysd/ai/RuiCameraApi.java line 444: MotorFrontStep
- com/hysd/ai/RuiCameraApi.java line 453: MotorBackStep
- com/hysd/ai/RuiCameraApi.java line 462: MotorFrontTofStep
- com/hysd/ai/RuiCameraApi.java line 472: MotorBackTofStep
- com/hysd/ai/RuiCameraApi.java line 482: MotorStop
- com/hysd/ai/RuiCameraApi.java line 601: startTof
- com/trd/sdk/impl/MotorCtrlImpl.java line 13: getMotorCtrl
- com/trd/sdk/impl/MotorCtrlImpl.java line 33: getMotorCtrl
- com/trd/sdk/impl/TofCtrlImpl.java line 13: getTofCtrl
- com/trd/sdk/impl/TofCtrlImpl.java line 33: getTofCtrl

## Keystone geometry — KeystoneCorrection

- com/rjpj/tcorrection/HVKeystoneActivity.java :: setContentView(com.rjpj.tcorrection.R.layout.activity_hvkeystone_correction)
- com/rjpj/tcorrection/I2CDevice.java :: public native int open(java.lang.String str, int i) [native]
- com/rjpj/tcorrection/I2CDevice.java :: public native int readRegister(int i) [native]
- com/rjpj/tcorrection/I2CDevice.java :: public native int writeRegister(int i, int i2) [native]
- com/rjpj/tcorrection/I2CDevice.java :: public native void close() [native]
- com/rjpj/tcorrection/KeystoneUtil.java :: if (i2CDevice != null)
- com/rjpj/tcorrection/KeystoneUtil.java :: if (i2CDevice != null)
- com/rjpj/tcorrection/KeystoneUtil.java :: if (i2CDevice2.open("/dev/i2c-1", 90) == 0)
- com/rjpj/tcorrection/KeystoneUtil.java :: if (projectorMirrorMode == 1 || projectorMirrorMode == 3)
- com/rjpj/tcorrection/KeystoneUtil.java :: if (projectorMirrorMode == 1 || projectorMirrorMode == 3)
- com/rjpj/tcorrection/KeystoneUtil.java :: if (projectorMirrorMode == 1 || projectorMirrorMode == 3)
- com/rjpj/tcorrection/KeystoneUtil.java :: if (projectorMirrorMode == 1 || projectorMirrorMode == 3)
- com/rjpj/tcorrection/KeystoneUtil.java :: private KeystoneUtil()
- com/rjpj/tcorrection/KeystoneUtil.java :: private void updateKeystoneProperties()
- com/rjpj/tcorrection/KeystoneUtil.java :: private void writeParcelToFlinger(int i) throws java.lang.Throwable
- com/rjpj/tcorrection/KeystoneUtil.java :: public int getProjectorMirrorMode()
- com/rjpj/tcorrection/KeystoneUtil.java :: public static com.rjpj.tcorrection.KeystoneUtil getInstance()
- com/rjpj/tcorrection/KeystoneUtil.java :: public void resetKeystone() throws java.lang.Throwable
- com/rjpj/tcorrection/KeystoneUtil.java :: public void setLTOffset(int i, int i2) throws java.lang.Throwable
- com/rjpj/tcorrection/KeystoneUtil.java :: public void setRTOffset(int i, int i2) throws java.lang.Throwable
- com/rjpj/tcorrection/KeystoneUtil.java :: synchronized (com.rjpj.tcorrection.KeystoneUtil.class)
- com/rjpj/tcorrection/KeystoneUtil.java :: updateKeystoneProperties()
- com/rjpj/tcorrection/KeystoneUtil.java :: updateKeystoneProperties()
- com/rjpj/tcorrection/KeystoneUtil.java :: writeParcelToFlinger(0)
- com/rjpj/tcorrection/KeystoneUtil.java :: writeParcelToFlinger(0)
- com/rjpj/tcorrection/KeystoneUtil.java :: writeParcelToFlinger(1)
- com/rjpj/tcorrection/KeystoneUtil.java :: writeParcelToFlinger(2)
- com/rjpj/tcorrection/KeystoneUtil.java :: writeParcelToFlinger(3)
- com/rjpj/tcorrection/KeystoneUtil.java :: writeParcelToFlinger(4)
- com/trd/framework/IProjectorCtrl.java :: public void onKeyStoneValue(int i, int i2, int i3, int i4, int i5, int i6, int i7, int i8) throws android.os.RemoteException
- com/trd/framework/IProjectorCtrl.java :: void onKeyStoneValue(int i, int i2, int i3, int i4, int i5, int i6, int i7, int i8) throws android.os.RemoteException
- com/trd/sdk/ProjectorCtrl.java :: void onKeyStoneValue(int i, int i2, int i3, int i4, int i5, int i6, int i7, int i8)
- com/trd/sdk/impl/ProjectorCtrlImpl.java :: public void onKeyStoneValue(int i, int i2, int i3, int i4, int i5, int i6, int i7, int i8)

Call-site identifiers (without proprietary Java body):

- com/rjpj/tcorrection/KeystoneUtil.java line 57: writeParcelToFlinger
- com/rjpj/tcorrection/KeystoneUtil.java line 64: writeParcelToFlinger
- com/rjpj/tcorrection/KeystoneUtil.java line 71: writeParcelToFlinger
- com/rjpj/tcorrection/KeystoneUtil.java line 78: writeParcelToFlinger
- com/rjpj/tcorrection/KeystoneUtil.java line 90: writeParcelToFlinger
- com/rjpj/tcorrection/KeystoneUtil.java line 104: writeParcelToFlinger
- com/rjpj/tcorrection/KeystoneUtil.java line 107: writeParcelToFlinger

## HDMI inputs — KuSourceRJ

- com/coolux/source/MainActivity.java :: cancelFocus()
- com/coolux/source/MainActivity.java :: hd2Focus()
- com/coolux/source/MainActivity.java :: hdFocus()
- com/coolux/source/MainActivity.java :: if (this.hdmiNum == 2)
- com/coolux/source/MainActivity.java :: if (view.getId() == com.coolux.source.R.id.hdmi_layout)
- com/coolux/source/MainActivity.java :: if (view.getId() == com.coolux.source.R.id.hdmi_layout)
- com/coolux/source/MainActivity.java :: private void cancelFocus()
- com/coolux/source/MainActivity.java :: private void hd2Focus()
- com/coolux/source/MainActivity.java :: private void hdFocus()
- com/coolux/source/MainActivity.java :: public void enterFocus(android.view.View view)
- com/coolux/source/MainActivity.java :: public void loseFocus(android.view.View view)
- com/coolux/source/MainActivity.java :: public void onFocusChange(android.view.View view, boolean z)
- com/coolux/source/MainActivity.java :: setContentView(com.coolux.source.R.layout.activity_source)
- com/coolux/source/activity/AllAppAutoActivity.java :: if (!com.coolux.source.constant.Constans.DATA_KEY.equals(str) || (list = (java.util.List) obj) == null || list.size() <= 0)
- com/coolux/source/activity/AllAppAutoActivity.java :: setContentView(com.coolux.source.R.layout.activity_all_apps_auto)
- com/coolux/source/activity/AuthorizationActivity.java :: setContentView(com.coolux.source.R.layout.activity_authorization)
- com/coolux/source/activity/AutomaticAdmissionActivity.java :: if (view.getId() == com.coolux.source.R.id.admission_start)
- com/coolux/source/activity/AutomaticAdmissionActivity.java :: setContentView(com.coolux.source.R.layout.activity_automatic_admission)
- com/coolux/source/activity/BootSoureActivity.java :: getBootSource()
- com/coolux/source/activity/BootSoureActivity.java :: if ("USB".equals(this.source_idString))
- com/coolux/source/activity/BootSoureActivity.java :: if (android.text.TextUtils.isEmpty(systemSource) || com.trd.common.bean.TrdTvInputSourceInfo.LABEL_HOME.equals(this.source_idString))
- com/coolux/source/activity/BootSoureActivity.java :: if (this.hdmiNum == 2)
- com/coolux/source/activity/BootSoureActivity.java :: if (this.source_idString.contains("com.mediatek.tvinput") && this.source_idString.contains("HW6"))
- com/coolux/source/activity/BootSoureActivity.java :: if (this.source_idString.contains("com.mediatek.tvinput") && this.source_idString.contains("HW7"))
- com/coolux/source/activity/BootSoureActivity.java :: if (view.getId() == com.coolux.source.R.id.android_source_layout)
- com/coolux/source/activity/BootSoureActivity.java :: if (view.getId() == com.coolux.source.R.id.auto_app_layout && keyEvent.getAction() == 0)
- com/coolux/source/activity/BootSoureActivity.java :: if (view.getId() == com.coolux.source.R.id.auto_app_layout)
- com/coolux/source/activity/BootSoureActivity.java :: if (view.getId() == com.coolux.source.R.id.hdmi2_source_layout)
- com/coolux/source/activity/BootSoureActivity.java :: if (view.getId() == com.coolux.source.R.id.hdmi_source_layout)
- com/coolux/source/activity/BootSoureActivity.java :: if (view.getId() == com.coolux.source.R.id.usb_source_layout)
- com/coolux/source/activity/BootSoureActivity.java :: private void getBootSource()
- com/coolux/source/activity/BootSoureActivity.java :: private void setBootSource(int i)
- com/coolux/source/activity/BootSoureActivity.java :: private void viewBootSource()
- com/coolux/source/activity/BootSoureActivity.java :: setBootSource(i)
- com/coolux/source/activity/BootSoureActivity.java :: setContentView(com.coolux.source.R.layout.activity_boot_soure)
- com/coolux/source/activity/BootSoureActivity.java :: viewBootSource()
- com/coolux/source/activity/BootSoureActivity.java :: viewBootSource()
- com/coolux/source/activity/BootSoureActivity.java :: viewBootSource()
- com/coolux/source/activity/BootSoureActivityOld.java :: getBootSource()
- com/coolux/source/activity/BootSoureActivityOld.java :: if (android.text.TextUtils.isEmpty(this.source_idString) || com.trd.common.bean.TrdTvInputSourceInfo.LABEL_HOME.equals(this.source_idString))
- com/coolux/source/activity/BootSoureActivityOld.java :: if (this.hdmiNum == 2)
- com/coolux/source/activity/BootSoureActivityOld.java :: if (this.hdmiNum == 2)
- com/coolux/source/activity/BootSoureActivityOld.java :: if (this.source_idString.contains("com.mediatek.tvinput") && this.source_idString.contains("HW6"))
- com/coolux/source/activity/BootSoureActivityOld.java :: if (this.source_idString.contains("com.mediatek.tvinput") && this.source_idString.contains("HW7"))
- com/coolux/source/activity/BootSoureActivityOld.java :: if (view.getId() == com.coolux.source.R.id.android_source_layout)
- com/coolux/source/activity/BootSoureActivityOld.java :: if (view.getId() == com.coolux.source.R.id.auto_app_layout && keyEvent.getAction() == 0)
- com/coolux/source/activity/BootSoureActivityOld.java :: private void getBootSource()
- com/coolux/source/activity/BootSoureActivityOld.java :: private void setBootSource(int i)
- com/coolux/source/activity/BootSoureActivityOld.java :: private void viewBootSource()
- com/coolux/source/activity/BootSoureActivityOld.java :: private void viewBootSource1()
- com/coolux/source/activity/BootSoureActivityOld.java :: private void viewBootSource2()
- com/coolux/source/activity/BootSoureActivityOld.java :: setBootSource(i)
- com/coolux/source/activity/BootSoureActivityOld.java :: setContentView(com.coolux.source.R.layout.activity_boot_soure)
- com/coolux/source/activity/BootSoureActivityOld.java :: viewBootSource()
- com/coolux/source/activity/BootSoureActivityOld.java :: viewBootSource()
- com/coolux/source/activity/BootSoureActivityOld.java :: viewBootSource()
- com/coolux/source/activity/BootSoureActivityOld.java :: viewBootSource1()
- com/coolux/source/activity/BootSoureActivityOld.java :: viewBootSource2()
- com/coolux/source/activity/BrightActivity.java :: if (com.coolux.source.utils.SharedPreferencesTest.getInstance().getScreensaverModelValue(this.mContext) == 1)
- com/coolux/source/activity/BrightActivity.java :: if (com.coolux.source.utils.SharedPreferencesTest.getInstance().getScreensaverModelValue(this.mContext) == 1)
- com/coolux/source/activity/BrightActivity.java :: if (view.getId() == com.coolux.source.R.id.brightness_model_layout)
- com/coolux/source/activity/BrightActivity.java :: if (view.getId() == com.coolux.source.R.id.screensaver_layout)
- com/coolux/source/activity/BrightActivity.java :: setContentView(com.coolux.source.R.layout.activity_bright)
- com/coolux/source/activity/DustproofActivity.java :: setContentView(com.coolux.source.R.layout.activity_dusproof)
- com/coolux/source/activity/FanDetectionActivity.java :: setContentView(com.coolux.source.R.layout.activity_fan_detection)
- com/coolux/source/activity/HighTemperatureActivity.java :: setContentView(com.coolux.source.R.layout.activity_high_temperature)
- com/coolux/source/activity/KeystoneActivity.java :: clickAutoFocus()
- com/coolux/source/activity/KeystoneActivity.java :: clickAutomaticTrapezoid()
- com/coolux/source/activity/KeystoneActivity.java :: clickPowerOnAutoFocus()
- com/coolux/source/activity/KeystoneActivity.java :: clickPowerOnAutomaticTrapezoid()
- com/coolux/source/activity/KeystoneActivity.java :: clickTofAutofocus()
- com/coolux/source/activity/KeystoneActivity.java :: if (com.coolux.source.utils.ReflectionUtils.getInstance().isDPLSTOF())
- com/coolux/source/activity/KeystoneActivity.java :: if (this.autoFocus.equals("1"))
- com/coolux/source/activity/KeystoneActivity.java :: if (this.autoFocus.equals("1"))
- com/coolux/source/activity/KeystoneActivity.java :: if (this.automaticTrapezoid.equals("1"))
- com/coolux/source/activity/KeystoneActivity.java :: if (this.automaticTrapezoid.equals("1"))
- com/coolux/source/activity/KeystoneActivity.java :: if (this.powerOnAutoFocus.equals("1"))
- com/coolux/source/activity/KeystoneActivity.java :: if (this.powerOnAutoFocus.equals("1"))
- com/coolux/source/activity/KeystoneActivity.java :: if (this.powerOnAutomaticTrapezoid.equals("1"))
- com/coolux/source/activity/KeystoneActivity.java :: if (this.powerOnAutomaticTrapezoid.equals("1"))
- com/coolux/source/activity/KeystoneActivity.java :: if (this.tofAutofocus.equals("0"))
- com/coolux/source/activity/KeystoneActivity.java :: if (this.tofAutofocus.equals("1"))
- com/coolux/source/activity/KeystoneActivity.java :: if (view.getId() == com.coolux.source.R.id.auto_focus_layout)
- com/coolux/source/activity/KeystoneActivity.java :: if (view.getId() == com.coolux.source.R.id.automatic_admission_layout && keyEvent.getAction() == 0)
- com/coolux/source/activity/KeystoneActivity.java :: if (view.getId() == com.coolux.source.R.id.automatic_admission_layout)
- com/coolux/source/activity/KeystoneActivity.java :: if (view.getId() == com.coolux.source.R.id.automatic_trapezoid_layout)
- com/coolux/source/activity/KeystoneActivity.java :: if (view.getId() == com.coolux.source.R.id.four_point_layout)
- com/coolux/source/activity/KeystoneActivity.java :: if (view.getId() == com.coolux.source.R.id.keystone_layout)
- com/coolux/source/activity/KeystoneActivity.java :: if (view.getId() == com.coolux.source.R.id.power_on_auto_fouce_layout)
- com/coolux/source/activity/KeystoneActivity.java :: if (view.getId() == com.coolux.source.R.id.tof_autofocus_layout)
- com/coolux/source/activity/KeystoneActivity.java :: isViewTofAutofocus()
- com/coolux/source/activity/KeystoneActivity.java :: private void clickAutoFocus()
- com/coolux/source/activity/KeystoneActivity.java :: private void clickAutomaticTrapezoid()
- com/coolux/source/activity/KeystoneActivity.java :: private void clickPowerOnAutoFocus()
- com/coolux/source/activity/KeystoneActivity.java :: private void clickPowerOnAutomaticTrapezoid()
- com/coolux/source/activity/KeystoneActivity.java :: private void clickTofAutofocus()
- com/coolux/source/activity/KeystoneActivity.java :: private void isViewTofAutofocus()
- com/coolux/source/activity/KeystoneActivity.java :: private void viewAutoFocus()
- com/coolux/source/activity/KeystoneActivity.java :: private void viewAutomaticTrapezoid()
- com/coolux/source/activity/KeystoneActivity.java :: private void viewPowerOnAutoFocus()

Call-site identifiers (without proprietary Java body):

- com/coolux/source/utils/ImageUtils.java line 117: setBootSource
- com/coolux/source/utils/ImageUtils.java line 469: setTofAutofocus
- com/coolux/source/activity/AllAppAutoActivity.java line 81: setBootSource
- com/coolux/source/activity/BootSoureActivityOld.java line 76: setBootSource
- com/coolux/source/activity/BootSoureActivityOld.java line 77: setBootSource
- com/coolux/source/activity/BootSoureActivityOld.java line 160: setBootSource
- com/coolux/source/activity/BootSoureActivity.java line 78: setBootSource
- com/coolux/source/activity/BootSoureActivity.java line 79: setBootSource
- com/coolux/source/activity/BootSoureActivity.java line 154: setBootSource
- com/coolux/source/activity/KeystoneActivity.java line 157: setTofAutofocus

## Binder control interface — trdmiddle

- com/trd/android/api/MotorCtrlSetting.java :: public abstract int GetMotorStatus()
- com/trd/android/api/MotorCtrlSetting.java :: public abstract int SetMotorCtrl(int i2, int i3)
- com/trd/android/api/MotorCtrlSetting.java :: public abstract int SetMotorPhaseCtrl(int i2)
- com/trd/android/api/impl/MotorCtrlSettingImpl.java :: if (motorSettingImplinstance == null)
- com/trd/android/api/impl/MotorCtrlSettingImpl.java :: if (motorSettingImplinstance == null)
- com/trd/android/api/impl/MotorCtrlSettingImpl.java :: private MotorCtrlSettingImpl()
- com/trd/android/api/impl/MotorCtrlSettingImpl.java :: public int GetMotorStatus()
- com/trd/android/api/impl/MotorCtrlSettingImpl.java :: public int SetMotorCtrl(int i2, int i3)
- com/trd/android/api/impl/MotorCtrlSettingImpl.java :: public int SetMotorPhaseCtrl(int i2)
- com/trd/android/api/impl/MotorCtrlSettingImpl.java :: public static com.trd.android.api.impl.MotorCtrlSettingImpl getInstance()
- com/trd/android/api/impl/MotorCtrlSettingImpl.java :: synchronized (com.trd.android.api.impl.MotorCtrlSettingImpl.class)
- com/trd/framework/TrdSystemService.java :: public com.trd.framework.b getMotorCtrl()
- com/trd/framework/TrdSystemService.java :: public com.trd.framework.h getTofCtrl()
- com/trd/framework/TrdSystemService.java :: public static com.trd.framework.tof.TofCtrlService l()
- com/trd/framework/tof/TofController.java :: private TofController(com.trd.framework.tof.TofCtrlService tofCtrlService)
- com/trd/framework/tof/TofController.java :: public static com.trd.framework.tof.TofController create(com.trd.framework.tof.TofCtrlService tofCtrlService)
- com/trd/framework/tof/TofCtrlService.java :: if (this.mTofDataListenerRecords.isEmpty())
- com/trd/framework/tof/TofCtrlService.java :: if (tofControllerCreate == null)
- com/trd/framework/tof/TofCtrlService.java :: public TofCtrlService()
- com/trd/framework/tof/TofCtrlService.java :: public TofCtrlService(android.content.Context context, android.os.Handler handler)
- com/trd/framework/tof/TofCtrlService.java :: public TofDataListenerRecord(com.trd.framework.i iVar)
- com/trd/framework/tof/TofCtrlService.java :: public boolean handleTofCommand(com.trd.framework.tof.TofMessage tofMessage)
- com/trd/framework/tof/TofCtrlService.java :: public boolean invokeTofDataListenersOnReceived(int i2, int i3, byte[] bArr)
- com/trd/framework/tof/TofCtrlService.java :: public int SetTofStatus(int i2)
- com/trd/framework/tof/TofCtrlService.java :: public int[] readTofData()
- com/trd/framework/tof/TofCtrlService.java :: public void addTofDataListener(com.trd.framework.i iVar)
- com/trd/framework/tof/TofCtrlService.java :: return invokeTofDataListenersOnReceived(tofMessage.getType(), tofMessage.getCount(), tofMessage.getParams())
- com/trd/framework/tof/TofCtrlService.java :: synchronized (com.trd.framework.tof.TofCtrlService.this.mLock)

## Event service — trdservice

- com/trd/sdk/TrdSystemManager.java :: public static com.trd.sdk.TrdSystemManager getInstance()
- com/trd/sdk/TrdSystemManager.java :: synchronized (com.trd.sdk.TrdSystemManager.class)
- com/trd/service/ITrdService.java :: attachInterface(this, "com.trd.service.ITrdService")
- com/trd/service/ui/RJFocusDialog.java :: centerFocusPics()
- com/trd/service/ui/RJFocusDialog.java :: focus_far()
- com/trd/service/ui/RJFocusDialog.java :: focus_near()
- com/trd/service/ui/RJFocusDialog.java :: public RJFocusDialog(android.content.Context context)
- com/trd/service/ui/RJFocusDialog.java :: public void centerFocusPics()
- com/trd/service/ui/RJFocusDialog.java :: public void focus_far()
- com/trd/service/ui/RJFocusDialog.java :: public void focus_near()
- com/trd/service/ui/RJFocusDialog.java :: public void showFocus(int i)
- com/trd/service/ui/RJFocusDialog.java :: setContentView(com.trd.service.R.layout.rj_focus_dialog)

## OEM settings — KuSettings

- com/bumptech/glide/load/ResourceDecoder.java :: com.bumptech.glide.load.engine.Resource<Z> decode(T t, int i, int i2, com.bumptech.glide.load.Options options) throws java.io.IOException
- com/bumptech/glide/load/engine/ActiveResources.java :: ActiveResources(boolean isActiveResourceRetentionAllowed)
- com/bumptech/glide/load/engine/ActiveResources.java :: ActiveResources(boolean isActiveResourceRetentionAllowed, java.util.concurrent.Executor monitorClearedResourcesExecutor)
- com/bumptech/glide/load/engine/ActiveResources.java :: ResourceWeakReference(com.bumptech.glide.load.Key key, com.bumptech.glide.load.engine.EngineResource<?> referent, java.lang.ref.ReferenceQueue<? super com.bumptech.glide.load.engine.EngineResource<?>> queue, boolean isActiveResourceRetentionAllowed)
- com/bumptech/glide/load/engine/ActiveResources.java :: if (ref.isCacheable && ref.resource != null)
- com/bumptech/glide/load/engine/ActiveResources.java :: if (referent.isMemoryCacheable() && isActiveResourceRetentionAllowed)
- com/bumptech/glide/load/engine/ActiveResources.java :: synchronized com.bumptech.glide.load.engine.EngineResource<?> get(com.bumptech.glide.load.Key key)
- com/bumptech/glide/load/engine/ActiveResources.java :: synchronized void activate(com.bumptech.glide.load.Key key, com.bumptech.glide.load.engine.EngineResource<?> resource)
- com/bumptech/glide/load/engine/ActiveResources.java :: this(isActiveResourceRetentionAllowed, java.util.concurrent.Executors.newSingleThreadExecutor(new java.util.concurrent.ThreadFactory()
- com/bumptech/glide/load/engine/ActiveResources.java :: void cleanupActiveReference(com.bumptech.glide.load.engine.ActiveResources.ResourceWeakReference ref)
- com/bumptech/glide/load/engine/ActiveResources.java :: void onResourceDequeued()
- com/bumptech/glide/load/engine/ActiveResources.java :: void setDequeuedResourceCallback(com.bumptech.glide.load.engine.ActiveResources.DequeuedResourceCallback cb)
- com/bumptech/glide/load/engine/ActiveResources.java :: void setListener(com.bumptech.glide.load.engine.EngineResource.ResourceListener listener)
- com/bumptech/glide/load/engine/EngineResource.java :: EngineResource(com.bumptech.glide.load.engine.Resource<Z> toWrap, boolean isMemoryCacheable, boolean isRecyclable, com.bumptech.glide.load.Key key, com.bumptech.glide.load.engine.EngineResource.ResourceListener listener)
- com/bumptech/glide/load/engine/EngineResource.java :: com.bumptech.glide.load.engine.Resource<Z> getResource()
- com/bumptech/glide/load/engine/EngineResource.java :: public java.lang.Class<Z> getResourceClass()
- com/bumptech/glide/load/engine/EngineResource.java :: void onResourceReleased(com.bumptech.glide.load.Key key, com.bumptech.glide.load.engine.EngineResource<?> engineResource)
- com/bumptech/glide/load/engine/LockedResource.java :: LockedResource()
- com/bumptech/glide/load/engine/LockedResource.java :: private void init(com.bumptech.glide.load.engine.Resource<Z> toWrap)
- com/bumptech/glide/load/engine/LockedResource.java :: public com.bumptech.glide.load.engine.LockedResource<?> create()
- com/bumptech/glide/load/engine/LockedResource.java :: public java.lang.Class<Z> getResourceClass()
- com/bumptech/glide/load/engine/LockedResource.java :: static <Z> com.bumptech.glide.load.engine.LockedResource<Z> obtain(com.bumptech.glide.load.engine.Resource<Z> resource)
- com/bumptech/glide/load/engine/Resource.java :: java.lang.Class<Z> getResourceClass()
- com/bumptech/glide/load/engine/ResourceCacheGenerator.java :: ResourceCacheGenerator(com.bumptech.glide.load.engine.DecodeHelper<?> helper, com.bumptech.glide.load.engine.DataFetcherGenerator.FetcherReadyCallback cb)
- com/bumptech/glide/load/engine/ResourceCacheGenerator.java :: if (i2 >= resourceClasses.size())
- com/bumptech/glide/load/engine/ResourceCacheGenerator.java :: if (i3 >= sourceIds.size())
- com/bumptech/glide/load/engine/ResourceCacheGenerator.java :: if (resourceClasses.isEmpty())
- com/bumptech/glide/load/engine/ResourceCacheGenerator.java :: if (sourceIds.isEmpty())
- com/bumptech/glide/load/engine/ResourceCacheKey.java :: if (!(o instanceof com.bumptech.glide.load.engine.ResourceCacheKey))
- com/bumptech/glide/load/engine/ResourceCacheKey.java :: private byte[] getResourceClassBytes()
- com/bumptech/glide/load/engine/ResourceCacheKey.java :: return (((result2 * 31) + this.decodedResourceClass.hashCode()) * 31) + this.options.hashCode()
- com/bumptech/glide/load/engine/ResourceRecycler.java :: ResourceRecycler()
- com/bumptech/glide/load/engine/ResourceRecycler.java :: ResourceRecyclerCallback()
- com/bumptech/glide/load/engine/ResourceRecycler.java :: synchronized void recycle(com.bumptech.glide.load.engine.Resource<?> resource, boolean forceNextFrame)
- com/bumptech/glide/load/engine/SourceGenerator.java :: SourceGenerator(com.bumptech.glide.load.engine.DecodeHelper<?> helper, com.bumptech.glide.load.engine.DataFetcherGenerator.FetcherReadyCallback cb)
- com/bumptech/glide/load/engine/SourceGenerator.java :: if (com.bumptech.glide.load.engine.SourceGenerator.this.isCurrentRequest(toStart))
- com/bumptech/glide/load/engine/SourceGenerator.java :: if (com.bumptech.glide.load.engine.SourceGenerator.this.isCurrentRequest(toStart))
- com/bumptech/glide/load/engine/SourceGenerator.java :: if (data != null && diskCacheStrategy.isDataCacheable(loadData.fetcher.getDataSource()))
- com/bumptech/glide/load/engine/SourceGenerator.java :: if (this.loadData != null && (this.helper.getDiskCacheStrategy().isDataCacheable(this.loadData.fetcher.getDataSource()) || this.helper.hasLoadPath(this.loadData.fetcher.getDataClass())))
- com/bumptech/glide/load/engine/SourceGenerator.java :: public void onDataFetcherFailed(com.bumptech.glide.load.Key sourceKey, java.lang.Exception e, com.bumptech.glide.load.data.DataFetcher<?> fetcher, com.bumptech.glide.load.DataSource dataSource)
- com/bumptech/glide/load/engine/SourceGenerator.java :: public void onDataFetcherReady(com.bumptech.glide.load.Key sourceKey, java.lang.Object data, com.bumptech.glide.load.data.DataFetcher<?> fetcher, com.bumptech.glide.load.DataSource dataSource, com.bumptech.glide.load.Key attemptedKey)
- com/bumptech/glide/load/engine/cache/LruResourceCache.java :: if (resourceRemovedListener != null && item != null)
- com/bumptech/glide/load/engine/cache/LruResourceCache.java :: public LruResourceCache(long size)
- com/bumptech/glide/load/engine/cache/LruResourceCache.java :: public int getSize(com.bumptech.glide.load.engine.Resource<?> item)
- com/bumptech/glide/load/engine/cache/LruResourceCache.java :: public void onItemEvicted(com.bumptech.glide.load.Key key, com.bumptech.glide.load.engine.Resource<?> item)
- com/bumptech/glide/load/engine/cache/LruResourceCache.java :: public void setResourceRemovedListener(com.bumptech.glide.load.engine.cache.MemoryCache.ResourceRemovedListener listener)
- com/bumptech/glide/load/engine/cache/LruResourceCache.java :: return (com.bumptech.glide.load.engine.Resource) super.put(key, resource)
- com/bumptech/glide/load/engine/cache/LruResourceCache.java :: return (com.bumptech.glide.load.engine.Resource) super.remove(key)
- com/bumptech/glide/load/model/ResourceLoader.java :: private android.net.Uri getResourceUri(java.lang.Integer model)
- com/bumptech/glide/load/model/ResourceLoader.java :: public AssetFileDescriptorFactory(android.content.res.Resources resources)
- com/bumptech/glide/load/model/ResourceLoader.java :: public FileDescriptorFactory(android.content.res.Resources resources)
- com/bumptech/glide/load/model/ResourceLoader.java :: public ResourceLoader(android.content.res.Resources resources, com.bumptech.glide.load.model.ModelLoader<android.net.Uri, Data> uriLoader)
- com/bumptech/glide/load/model/ResourceLoader.java :: public StreamFactory(android.content.res.Resources resources)
- com/bumptech/glide/load/model/ResourceLoader.java :: public UriFactory(android.content.res.Resources resources)
- com/bumptech/glide/load/resource/ImageDecoderResourceDecoder.java :: if (android.util.Log.isLoggable(com.bumptech.glide.load.resource.ImageDecoderResourceDecoder.TAG, 2))
- com/bumptech/glide/load/resource/ImageDecoderResourceDecoder.java :: if (com.bumptech.glide.load.resource.ImageDecoderResourceDecoder.this.hardwareConfigState.isHardwareConfigAllowed(requestedWidth, requestedHeight, isHardwareConfigAllowed, false))
- com/bumptech/glide/load/resource/ImageDecoderResourceDecoder.java :: protected abstract com.bumptech.glide.load.engine.Resource<T> decode(android.graphics.ImageDecoder.Source source, int i, int i2, android.graphics.ImageDecoder.OnHeaderDecodedListener onHeaderDecodedListener) throws java.io.IOException
- com/bumptech/glide/load/resource/ImageDecoderResourceDecoder.java :: public final boolean handles(android.graphics.ImageDecoder.Source source, com.bumptech.glide.load.Options options)
- com/bumptech/glide/load/resource/ImageDecoderResourceDecoder.java :: public final com.bumptech.glide.load.engine.Resource<T> decode(android.graphics.ImageDecoder.Source source, final int requestedWidth, final int requestedHeight, com.bumptech.glide.load.Options options) throws java.io.IOException
- com/bumptech/glide/load/resource/ImageDecoderResourceDecoder.java :: public void onHeaderDecoded(android.graphics.ImageDecoder decoder, android.graphics.ImageDecoder.ImageInfo info, android.graphics.ImageDecoder.Source source2)
- com/bumptech/glide/load/resource/ImageDecoderResourceDecoder.java :: return decode(source, requestedWidth, requestedHeight, new android.graphics.ImageDecoder.OnHeaderDecodedListener()
- com/bumptech/glide/load/resource/SimpleResource.java :: public SimpleResource(T t)
- com/bumptech/glide/load/resource/SimpleResource.java :: public java.lang.Class<T> getResourceClass()
- com/bumptech/glide/load/resource/UnitTransformation.java :: public com.bumptech.glide.load.engine.Resource<T> transform(android.content.Context context, com.bumptech.glide.load.engine.Resource<T> resource, int outWidth, int outHeight)
- com/bumptech/glide/load/resource/UnitTransformation.java :: public static <T> com.bumptech.glide.load.resource.UnitTransformation<T> get()
- com/bumptech/glide/load/resource/bitmap/BitmapDrawableDecoder.java :: public BitmapDrawableDecoder(android.content.Context context, com.bumptech.glide.load.ResourceDecoder<DataType, android.graphics.Bitmap> decoder)
- com/bumptech/glide/load/resource/bitmap/BitmapDrawableDecoder.java :: public BitmapDrawableDecoder(android.content.res.Resources resources, com.bumptech.glide.load.ResourceDecoder<DataType, android.graphics.Bitmap> decoder)
- com/bumptech/glide/load/resource/bitmap/BitmapDrawableDecoder.java :: public BitmapDrawableDecoder(android.content.res.Resources resources, com.bumptech.glide.load.engine.bitmap_recycle.BitmapPool bitmapPool, com.bumptech.glide.load.ResourceDecoder<DataType, android.graphics.Bitmap> decoder)
- com/bumptech/glide/load/resource/bitmap/BitmapDrawableDecoder.java :: public boolean handles(DataType source, com.bumptech.glide.load.Options options) throws java.io.IOException
- com/bumptech/glide/load/resource/bitmap/BitmapDrawableDecoder.java :: public com.bumptech.glide.load.engine.Resource<android.graphics.drawable.BitmapDrawable> decode(DataType source, int width, int height, com.bumptech.glide.load.Options options) throws java.io.IOException
- com/bumptech/glide/load/resource/bitmap/BitmapDrawableDecoder.java :: this(context.getResources(), decoder)
- com/bumptech/glide/load/resource/bitmap/BitmapDrawableDecoder.java :: this(resources, decoder)
- com/bumptech/glide/load/resource/bitmap/BitmapDrawableEncoder.java :: public BitmapDrawableEncoder(com.bumptech.glide.load.engine.bitmap_recycle.BitmapPool bitmapPool, com.bumptech.glide.load.ResourceEncoder<android.graphics.Bitmap> encoder)
- com/bumptech/glide/load/resource/bitmap/BitmapDrawableEncoder.java :: public boolean encode(com.bumptech.glide.load.engine.Resource<android.graphics.drawable.BitmapDrawable> resource, java.io.File file, com.bumptech.glide.load.Options options)
- com/bumptech/glide/load/resource/bitmap/BitmapDrawableResource.java :: public BitmapDrawableResource(android.graphics.drawable.BitmapDrawable drawable, com.bumptech.glide.load.engine.bitmap_recycle.BitmapPool bitmapPool)
- com/bumptech/glide/load/resource/bitmap/BitmapDrawableResource.java :: public java.lang.Class<android.graphics.drawable.BitmapDrawable> getResourceClass()
- com/bumptech/glide/load/resource/bitmap/BitmapDrawableTransformation.java :: if (!(resource.get() instanceof android.graphics.drawable.BitmapDrawable))
- com/bumptech/glide/load/resource/bitmap/BitmapDrawableTransformation.java :: if (o instanceof com.bumptech.glide.load.resource.bitmap.BitmapDrawableTransformation)
- com/bumptech/glide/load/resource/bitmap/BitmapDrawableTransformation.java :: private static com.bumptech.glide.load.engine.Resource<android.graphics.drawable.BitmapDrawable> convertToBitmapDrawableResource(com.bumptech.glide.load.engine.Resource<android.graphics.drawable.Drawable> resource)
- com/bumptech/glide/load/resource/bitmap/BitmapDrawableTransformation.java :: private static com.bumptech.glide.load.engine.Resource<android.graphics.drawable.Drawable> convertToDrawableResource(com.bumptech.glide.load.engine.Resource<android.graphics.drawable.BitmapDrawable> toConvert)
- com/bumptech/glide/load/resource/bitmap/BitmapDrawableTransformation.java :: public com.bumptech.glide.load.engine.Resource<android.graphics.drawable.BitmapDrawable> transform(android.content.Context context, com.bumptech.glide.load.engine.Resource<android.graphics.drawable.BitmapDrawable> drawableResourceToTransform, int outWidth, int outHeight)
- com/bumptech/glide/load/resource/bitmap/BitmapDrawableTransformation.java :: return convertToBitmapDrawableResource(transformed)
- com/bumptech/glide/load/resource/bitmap/BitmapEncoder.java :: public boolean encode(com.bumptech.glide.load.engine.Resource<android.graphics.Bitmap> resource, java.io.File file, com.bumptech.glide.load.Options options)
- com/bumptech/glide/load/resource/bitmap/BitmapImageDecoderResourceDecoder.java :: protected com.bumptech.glide.load.engine.Resource<android.graphics.Bitmap> decode(android.graphics.ImageDecoder.Source source, int requestedResourceWidth, int requestedResourceHeight, android.graphics.ImageDecoder.OnHeaderDecodedListener listener) throws java.io.IOException
- com/bumptech/glide/load/resource/bitmap/BitmapResource.java :: public BitmapResource(android.graphics.Bitmap bitmap, com.bumptech.glide.load.engine.bitmap_recycle.BitmapPool bitmapPool)
- com/bumptech/glide/load/resource/bitmap/BitmapResource.java :: public java.lang.Class<android.graphics.Bitmap> getResourceClass()
- com/bumptech/glide/load/resource/bitmap/BitmapResource.java :: public static com.bumptech.glide.load.resource.bitmap.BitmapResource obtain(android.graphics.Bitmap bitmap, com.bumptech.glide.load.engine.bitmap_recycle.BitmapPool bitmapPool)
- com/bumptech/glide/load/resource/bitmap/BitmapTransformation.java :: public final com.bumptech.glide.load.engine.Resource<android.graphics.Bitmap> transform(android.content.Context context, com.bumptech.glide.load.engine.Resource<android.graphics.Bitmap> resource, int outWidth, int outHeight)
- com/bumptech/glide/load/resource/bitmap/BitmapTransitionOptions.java :: public com.bumptech.glide.load.resource.bitmap.BitmapTransitionOptions crossFade()
- com/bumptech/glide/load/resource/bitmap/BitmapTransitionOptions.java :: public com.bumptech.glide.load.resource.bitmap.BitmapTransitionOptions crossFade(com.bumptech.glide.request.transition.DrawableCrossFadeFactory drawableCrossFadeFactory)
- com/bumptech/glide/load/resource/bitmap/BitmapTransitionOptions.java :: public com.bumptech.glide.load.resource.bitmap.BitmapTransitionOptions crossFade(com.bumptech.glide.request.transition.DrawableCrossFadeFactory.Builder builder)
- com/bumptech/glide/load/resource/bitmap/BitmapTransitionOptions.java :: public com.bumptech.glide.load.resource.bitmap.BitmapTransitionOptions crossFade(int duration)
- com/bumptech/glide/load/resource/bitmap/BitmapTransitionOptions.java :: public com.bumptech.glide.load.resource.bitmap.BitmapTransitionOptions transitionUsing(com.bumptech.glide.request.transition.TransitionFactory<android.graphics.drawable.Drawable> drawableCrossFadeFactory)
- com/bumptech/glide/load/resource/bitmap/BitmapTransitionOptions.java :: public static com.bumptech.glide.load.resource.bitmap.BitmapTransitionOptions with(com.bumptech.glide.request.transition.TransitionFactory<android.graphics.Bitmap> transitionFactory)
- com/bumptech/glide/load/resource/bitmap/BitmapTransitionOptions.java :: public static com.bumptech.glide.load.resource.bitmap.BitmapTransitionOptions withCrossFade()
- com/bumptech/glide/load/resource/bitmap/BitmapTransitionOptions.java :: public static com.bumptech.glide.load.resource.bitmap.BitmapTransitionOptions withCrossFade(com.bumptech.glide.request.transition.DrawableCrossFadeFactory drawableCrossFadeFactory)
- com/bumptech/glide/load/resource/bitmap/BitmapTransitionOptions.java :: public static com.bumptech.glide.load.resource.bitmap.BitmapTransitionOptions withCrossFade(com.bumptech.glide.request.transition.DrawableCrossFadeFactory.Builder builder)
- com/bumptech/glide/load/resource/bitmap/BitmapTransitionOptions.java :: public static com.bumptech.glide.load.resource.bitmap.BitmapTransitionOptions withCrossFade(int duration)
- com/bumptech/glide/load/resource/bitmap/BitmapTransitionOptions.java :: public static com.bumptech.glide.load.resource.bitmap.BitmapTransitionOptions withWrapped(com.bumptech.glide.request.transition.TransitionFactory<android.graphics.drawable.Drawable> drawableCrossFadeFactory)
- com/bumptech/glide/load/resource/bitmap/ByteBufferBitmapDecoder.java :: public ByteBufferBitmapDecoder(com.bumptech.glide.load.resource.bitmap.Downsampler downsampler)

## Relevant JNI/native exports


### system_a/system/lib/libfactoryi2c_jni.so

- SHA256: 7f4aa383f1346fa16c04d5569d6cdd2da4b27e8c49f5100e3b1c236c5635e258
- Dependencies: libc++.so, libc.so, libdl.so, liblog.so, libm.so, libnativehelper.so
- Relevant dynamic symbol names: 4
- Java_mediatek_util_I2CDevice_close
- Java_mediatek_util_I2CDevice_open
- Java_mediatek_util_I2CDevice_readRegister
- Java_mediatek_util_I2CDevice_writeRegister

### system_a/system/lib/libi2c_jni.so

- SHA256: 105cd91625968377c91c8b79adc8e84d416ae3d32e9839da0be7511c1f76d491
- Dependencies: libc++.so, libc.so, libdl.so, liblog.so, libm.so, libnativehelper.so
- Relevant dynamic symbol names: 4
- Java_com_rjpj_tcorrection_I2CDevice_close
- Java_com_rjpj_tcorrection_I2CDevice_open
- Java_com_rjpj_tcorrection_I2CDevice_readRegister
- Java_com_rjpj_tcorrection_I2CDevice_writeRegister

### system_a/system/lib/librjpj_private_function.so

- SHA256: e436a1e31c3f7c49fb0e52894b83a12eb7a387b68144400ed24271785f1ae0d3
- Dependencies: libc++.so, libc.so, libdl.so, liblog.so, libm.so, libnativehelper.so
- Relevant dynamic symbol names: 18
- Java_com_trd_service_jni_MotorJNI_GetLimiterBack
- Java_com_trd_service_jni_MotorJNI_GetLimiterFront
- Java_com_trd_service_jni_MotorJNI_GetMissStep
- Java_com_trd_service_jni_MotorJNI_GetPwrOnStep
- Java_com_trd_service_jni_MotorJNI_GetResetStep
- Java_com_trd_service_jni_MotorJNI_GetReturnCnt
- Java_com_trd_service_jni_MotorJNI_GetRunStep
- Java_com_trd_service_jni_MotorJNI_GetSumStep
- Java_com_trd_service_jni_MotorJNI_RunMotorBack
- Java_com_trd_service_jni_MotorJNI_RunMotorFront
- Java_com_trd_service_jni_MotorJNI_RunMotorStop
- Java_com_trd_service_jni_MotorJNI_SetMissStep
- Java_com_trd_service_jni_MotorJNI_SetPwrOnStep
- Java_com_trd_service_jni_MotorJNI_SetResetStep
- Java_com_trd_service_jni_MotorJNI_SetReturnCnt
- Java_com_trd_service_jni_MotorJNI_SetRunStep
- Java_com_trd_service_jni_MotorJNI_SetSumStep
- Java_com_trd_service_jni_MotorJNI_ioctl

### system_a/system/lib/libsettingsi2c_jni.so

- SHA256: d9a8d644b400153d2b53eaadd892af5715acaa9b65caa6d52e697277ab20e724
- Dependencies: libc++.so, libc.so, libdl.so, liblog.so, libm.so, libnativehelper.so
- Relevant dynamic symbol names: 4
- Java_com_android_tv_settings_uicustom_I2CDevice_close
- Java_com_android_tv_settings_uicustom_I2CDevice_open
- Java_com_android_tv_settings_uicustom_I2CDevice_readRegister
- Java_com_android_tv_settings_uicustom_I2CDevice_writeRegister

### system_a/system/lib/libtof_jni.so

- SHA256: 3bfb96ca96581c5e86efd0d2ac4b5f3c96be335bd5b5dd0bd87bf233495d1b85
- Dependencies: android.hidl.allocator@1.0.so, android.hidl.memory@1.0.so, libandroid_runtime.so, libbinder.so, libc++.so, libc.so, libcutils.so, libdl.so, libhidlbase.so, liblog.so, libm.so, libtrdclient.so, libtrdclient_imp.so, libutils.so, vendor.trd.hardware.hwtrd@1.0.so, vendor.trd.hardware.tof@1.0.so
- Relevant dynamic symbol names: 30
- Java_com_trd_framework_tof_TofController_registerNativeMethods
- _ZN6vendor3trd8hardware3tof4V1_012ITofCallback11linkToDeathERKN7android2spINS5_8hardware20hidl_death_recipientEEEy
- _ZN6vendor3trd8hardware3tof4V1_012ITofCallback12getDebugInfoENSt3__18functionIFvRKN7android4hidl4base4V1_09DebugInfoEEEE
- _ZN6vendor3trd8hardware3tof4V1_012ITofCallback12getHashChainENSt3__18functionIFvRKN7android8hardware8hidl_vecINS8_10hidl_arrayIhLj32EJEEEEEEEE
- _ZN6vendor3trd8hardware3tof4V1_012ITofCallback13unlinkToDeathERKN7android2spINS5_8hardware20hidl_death_recipientEEE
- _ZN6vendor3trd8hardware3tof4V1_012ITofCallback14interfaceChainENSt3__18functionIFvRKN7android8hardware8hidl_vecINS8_11hidl_stringEEEEEE
- _ZN6vendor3trd8hardware3tof4V1_012ITofCallback19interfaceDescriptorENSt3__18functionIFvRKN7android8hardware11hidl_stringEEEE
- _ZN6vendor3trd8hardware3tof4V1_012ITofCallback21notifySyspropsChangedEv
- _ZN6vendor3trd8hardware3tof4V1_012ITofCallback21setHALInstrumentationEv
- _ZN6vendor3trd8hardware3tof4V1_012ITofCallback4pingEv
- _ZN6vendor3trd8hardware3tof4V1_012ITofCallback5debugERKN7android8hardware11hidl_handleERKNS6_8hidl_vecINS6_11hidl_stringEEE
- _ZN6vendor3trd8hardware3tof4V1_04ITof10getServiceERKNSt3__112basic_stringIcNS5_11char_traitsIcEENS5_9allocatorIcEEEEb
- _ZN7android13TofController11ReadTofDataEv
- _ZN7android13TofController11TofCallback12onTofMessageERKN6vendor3trd8hardware3tof4V1_010TofMessageE
- _ZN7android13TofController11TofCallback14onHotplugEventERKN6vendor3trd8hardware3tof4V1_08TofEventE
- _ZN7android13TofController14tof_set_statusEi
- _ZN7android13TofControllerC1ENS_2spIN6vendor3trd8hardware3tof4V1_04ITofEEEP8_jobjectRKNS1_INS_6LooperEEE
- _ZN7android13TofControllerC2ENS_2spIN6vendor3trd8hardware3tof4V1_04ITofEEEP8_jobjectRKNS1_INS_6LooperEEE
- _ZN7android13TofControllerD1Ev
- _ZN7android13TofControllerD2Ev
- _ZN7android2spIN6vendor3trd8hardware3tof4V1_012ITofCallbackEED2Ev
- _ZN7android2spIN6vendor3trd8hardware3tof4V1_04ITofEED2Ev
- _ZN7android2spINS_15TofEventHandlerEED2Ev
- _ZTCN7android13TofController11TofCallbackE0_N6vendor3trd8hardware3tof4V1_012ITofCallbackE
- _ZTCN7android13TofController11TofCallbackE0_NS_4hidl4base4V1_05IBaseE
- _ZTCN7android15TofEventHandlerE0_NS_14MessageHandlerE
- _ZTTN7android13TofController11TofCallbackE
- _ZTTN7android15TofEventHandlerE
- _ZTVN7android13TofController11TofCallbackE
- _ZTVN7android15TofEventHandlerE

### system_a/system/lib/libtrd_jni.so

- SHA256: 7d409b1df3c2d9d0f46252b3efbea2f22007b4f7683bbd18f94de86338993df7
- Dependencies: android.hidl.allocator@1.0.so, android.hidl.memory@1.0.so, libbinder.so, libc++.so, libc.so, libcutils.so, libdl.so, libhidlbase.so, liblog.so, libm.so, libtrdclient.so, libtrdclient_imp.so, libutils.so, vendor.trd.hardware.hwtrd@1.0.so
- Relevant dynamic symbol names: 20
- _ZN14JNITrdListener17CallbackPostEventEP7_JNIEnvjPKvj
- _ZN14JNITrdListener6notifyEjPKvjS1_
- _ZN14JNITrdListenerC1EP7_JNIEnvP8_jobjectS3_
- _ZN14JNITrdListenerC2EP7_JNIEnvP8_jobjectS3_
- _ZN14JNITrdListenerD0Ev
- _ZN14JNITrdListenerD1Ev
- _ZN14JNITrdListenerD2Ev
- _ZN7android10TrdCreator12mITrdManagerE
- _ZN7android10TrdCreator16mITrdManagerLockE
- _ZN7android2spI14JNITrdListenerED2Ev
- _ZN7android2spINS_11ITofSettingEED2Ev
- _ZN7android2spINS_11ITrdManagerEED2Ev
- _ZN7android2spINS_12ITrdListenerEED2Ev
- _ZN7android2spINS_17IMotorCtrlSettingEED2Ev
- _ZN7android9TrdClient14registCallbackEPNS_18ITrdClientCallbackE
- _ZTC14JNITrdListener0_N7android12ITrdListenerE
- _ZTT14JNITrdListener
- _ZTV14JNITrdListener
- _ZTv0_n12_N14JNITrdListenerD0Ev
- _ZTv0_n12_N14JNITrdListenerD1Ev

### vendor_a/priv-app/trdmiddle/lib/arm/libtrdmiddle.so

- SHA256: 81f8c4c0508418153c4724384842fe1fe4e1e29fb11b69c3233ffc798cd142d0
- Dependencies: libc++_shared.so, libc.so, libdl.so, liblog.so, libm.so, libopencv_java4.so
- Relevant dynamic symbol names: 10
- Java_com_trd_framework_projector_TrapezoidUtil_AutoTrapezoidInit
- Java_com_trd_framework_projector_TrapezoidUtil_LeftRightIncrease
- Java_com_trd_framework_projector_TrapezoidUtil_SetLeftRightTrapezid
- Java_com_trd_framework_projector_TrapezoidUtil_SetUpDownTrapezid__F
- Java_com_trd_framework_projector_TrapezoidUtil_SetUpDownTrapezid__FFF
- Java_com_trd_framework_projector_TrapezoidUtil_SetUpDownTrapezid__FFFFFF
- Java_com_trd_framework_projector_TrapezoidUtil_UpDownTrapezidIncrease
- Java_com_trd_framework_projector_TrapezoidUtil_setEigen
- _Z14warp_projectorRNSt6__ndk16vectorIN2cv6Point_IiEENS_9allocatorIS3_EEEE
- _Z20trapezoid_initializev

## Bluetooth output routing evidence


### vendor_a/etc/audio_policy_configuration.xml

- A2DP mentions: 10
- LE audio mentions: 0
- The existence of a Bluetooth audio policy does not confirm simultaneous output to 2 A2DP devices.
- “primary”, “A2DP”, “remote_submix”, “USB”
- “devicePorts”: a list of device descriptors for all input and output devices accessible via this
- “mixPorts”: listing all output and input streams exposed by the audio HAL
- “routes”: list of possible connections between input and output devices or between stream and
- "route": is defined by an attribute:
- -"sink": the sink involved in this route
- -"sources": all the sources than can be connected to the sink via vis route
- defined in <devicePorts> section.
- <mixPorts>
- <mixPort name="primary output" role="source" flags="AUDIO_OUTPUT_FLAG_PRIMARY">
- </mixPort>
- <mixPort name="mmap_no_irq_out" role="source"
- </mixPort>
- <mixPort name="offload output" role="source"
- </mixPort>
- <mixPort name="hw_av_sync output" role="source"
- </mixPort>
- <mixPort name="primary input" role="sink">
- </mixPort>
- <mixPort name="tv input" role="sink">
- </mixPort>
- <mixPort name="hdmi input" role="sink">
- </mixPort>
- <mixPort name="line input" role="sink">
- </mixPort>

### vendor_a/etc/audio_policy_engine_configuration.xml

- A2DP mentions: 0
- LE audio mentions: 0
- The existence of a Bluetooth audio policy does not confirm simultaneous output to 2 A2DP devices.

### vendor_a/etc/audio_policy_engine_criteria.xml

- A2DP mentions: 0
- LE audio mentions: 0
- The existence of a Bluetooth audio policy does not confirm simultaneous output to 2 A2DP devices.

### vendor_a/etc/audio_policy_engine_criterion_types.xml

- A2DP mentions: 6
- LE audio mentions: 0
- The existence of a Bluetooth audio policy does not confirm simultaneous output to 2 A2DP devices.
- <value numerical="16" literal="BluetoothSco" android_type="0x10"/>
- <value numerical="32" literal="BluetoothScoHeadset" android_type="0x20"/>
- <value numerical="64" literal="BluetoothScoCarkit" android_type="0x40"/>
- <value numerical="128" literal="BluetoothA2dp" android_type="0x80"/>
- <value numerical="256" literal="BluetoothA2dpHeadphones" android_type="0x100"/>
- <value numerical="512" literal="BluetoothA2dpSpeaker" android_type="0x200"/>
- <value numerical="8" literal="BluetoothScoHeadset" android_type="0x80000008"/>
- <value numerical="131072" literal="BluetoothA2dp" android_type="0x80020000"/>
- <value numerical="67108864" literal="BluetoothBle" android_type="0x84000000"/>
- <value literal="ForceBtSco" numerical="3"/>
- <value literal="ForceBtA2dp" numerical="4"/>
- <value literal="ForceNoBtA2dp" numerical="10"/>
- <value literal="ForceBtSco" numerical="3"/>
- <value literal="ForceBtSco" numerical="3"/>

### vendor_a/etc/audio_policy_engine_default_stream_volumes.xml

- A2DP mentions: 0
- LE audio mentions: 0
- The existence of a Bluetooth audio policy does not confirm simultaneous output to 2 A2DP devices.

### vendor_a/etc/audio_policy_engine_product_strategies.xml

- A2DP mentions: 0
- LE audio mentions: 0
- The existence of a Bluetooth audio policy does not confirm simultaneous output to 2 A2DP devices.
- <AttributesGroup streamType="AUDIO_STREAM_BLUETOOTH_SCO" volumeGroup="bluetooth_sco">
- <Attributes> <Flags value="AUDIO_FLAG_SCO"/> </Attributes>

### vendor_a/etc/audio_policy_engine_stream_volumes.xml

- A2DP mentions: 0
- LE audio mentions: 0
- The existence of a Bluetooth audio policy does not confirm simultaneous output to 2 A2DP devices.
- <name>bluetooth_sco</name>

### vendor_a/etc/audio_policy_volumes.xml

- A2DP mentions: 0
- LE audio mentions: 0
- The existence of a Bluetooth audio policy does not confirm simultaneous output to 2 A2DP devices.
- <volume stream="AUDIO_STREAM_BLUETOOTH_SCO" deviceCategory="DEVICE_CATEGORY_HEADSET">
- <volume stream="AUDIO_STREAM_BLUETOOTH_SCO" deviceCategory="DEVICE_CATEGORY_SPEAKER">
- <volume stream="AUDIO_STREAM_BLUETOOTH_SCO" deviceCategory="DEVICE_CATEGORY_EARPIECE">
- <volume stream="AUDIO_STREAM_BLUETOOTH_SCO" deviceCategory="DEVICE_CATEGORY_EXT_MEDIA"

### vendor_a/etc/bluetooth_audio_policy_configuration.xml

- A2DP mentions: 0
- LE audio mentions: 0
- The existence of a Bluetooth audio policy does not confirm simultaneous output to 2 A2DP devices.
- <!-- Bluetooth Audio HAL Audio Policy Configuration file -->
- <module name="bluetooth" halVersion="2.0">
- <mixPorts>
- <mixPort name="hearing aid output" role="source">
- </mixPort>
- </mixPorts>
- <devicePorts>
- <devicePort tagName="BT Hearing Aid Out" type="AUDIO_DEVICE_OUT_HEARING_AID" role="sink"/>
- </devicePorts>
- <routes>
- <route type="mix" sink="BT Hearing Aid Out"
- </routes>

### vendor_a/etc/r_submix_audio_policy_configuration.xml

- A2DP mentions: 0
- LE audio mentions: 0
- The existence of a Bluetooth audio policy does not confirm simultaneous output to 2 A2DP devices.
- <mixPorts>
- <mixPort name="r_submix output" role="source">
- </mixPort>
- <mixPort name="r_submix input" role="sink">
- </mixPort>
- </mixPorts>
- <devicePorts>
- <devicePort tagName="Remote Submix Out" type="AUDIO_DEVICE_OUT_REMOTE_SUBMIX"  role="sink">
- </devicePort>
- <devicePort tagName="Remote Submix In" type="AUDIO_DEVICE_IN_REMOTE_SUBMIX"  role="source">
- </devicePort>
- </devicePorts>
- <routes>
- <route type="mix" sink="Remote Submix Out"
- <route type="mix" sink="r_submix input"
- </routes>

### vendor_a/etc/usb_audio_policy_configuration.xml

- A2DP mentions: 0
- LE audio mentions: 0
- The existence of a Bluetooth audio policy does not confirm simultaneous output to 2 A2DP devices.
- <mixPorts>
- <mixPort name="usb_device input" role="sink"/>
- </mixPorts>
- <devicePorts>
- <devicePort tagName="USB Device In" type="AUDIO_DEVICE_IN_USB_DEVICE" role="source"/>
- <devicePort tagName="USB Headset In" type="AUDIO_DEVICE_IN_USB_HEADSET" role="source"/>
- </devicePorts>
- <routes>
- <route type="mix" sink="usb_device input"
- </routes>

## Safe integration path

1. Prefer OEM settings activities and existing Binder service over direct hardware I2C access.
2. Identify actual package export flags and Binder service registration on a real device before implementing a companion.
3. Use separate hardware profiles for one-HDMI 8052 and two-HDMI/ToF 8054.
4. Bound motor steps, preserve emergency stop, and verify ToF presence and privileges before tests.
5. Treat HDMI selection, image options, and keystone separately; keep stock services until tested.
6. For two Bluetooth headphones, inspect A2DP source multiplicity, Android audio routing, BT stack and HAL. App-level audio duplication alone does not guarantee support.
7. Keep the stock, device-matched initial setup application. Do not import 8053 Provision or A2DP sink functionality.

## Limits

- Decompiled signatures and JNI exports are not a public supported SDK.
- Exact Binder permissions, I2C bus and register semantics are not yet determined.
- No OEM JNI method was executed; there was no flashing or calibration write.

