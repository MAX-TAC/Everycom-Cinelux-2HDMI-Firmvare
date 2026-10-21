# OEM KuSetupWizard versus KuSettings — source clone analysis

Source: SHA256-verified OTA RUIOS.8052.1.0.4. Reconstructed Java code was not published.
Identical normalized JADX classes are a strong similarity signal, not permission to remove either package.

## Packages and installed components

- KuSettings: com.my.settings; Java classes 3470; components {'activity': 11, 'provider': 1, 'receiver': 2, 'service': 2}
- KuSetupWizard: com.android.provision; Java classes 3471; components {'activity': 3, 'provider': 1, 'receiver': 1}

## Exact class-path overlap

- Common class paths: 3470
- Identical normalized Java classes: 3449
- Modified normalized classes: 21
- Unique to Settings: 0
- Unique to Wizard: 1
- Shared-class identity rate: 0.9939

### Classes with changed bodies
- androidx/appcompat/R.java
- androidx/cardview/R.java
- androidx/constraintlayout/widget/ConstraintSet.java
- androidx/constraintlayout/widget/R.java
- androidx/coordinatorlayout/R.java
- androidx/core/R.java
- androidx/core/app/AppLocalesStorageHelper.java
- androidx/customview/R.java
- androidx/drawerlayout/R.java
- androidx/loader/R.java
- androidx/recyclerview/R.java
- androidx/vectordrawable/R.java
- androidx/vectordrawable/animated/R.java
- androidx/viewpager/R.java
- androidx/viewpager2/R.java
- com/bumptech/glide/R.java
- com/google/android/material/R.java
- com/my/settings/R.java
- com/my/settings/activity/WarningActivity.java
- kotlinx/coroutines/CoroutineContextKt.java
- kotlinx/coroutines/SupervisorKt.java

### Classes unique to Setup Wizard
- com/android/provision/R.java

## Consequences

- A setup APK may contain a copy of the settings code but still have unique provisioning manifest, package UID, signatures and receivers.
- Inspect actual setup intent and DEVICE_PROVISIONED/USER_SETUP_COMPLETE handling before treating either APK as redundant.
- No app was removed, executed or modified.

