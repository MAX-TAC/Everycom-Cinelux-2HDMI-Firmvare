# Latest OTA 8052 vs stock 8054: launcher, store and setup wizard method changes

Original sources verified by SHA256. Decompiled Java normalized with the same hashing rules for both sides.
Changed method digest is a code fingerprint, not a confirmed bug nor proof that this method is used on the device.

## Summary

| APK | Exact APK SHA match | Same methods | Changed body | Added/removed | Own methods changed |
|---|---|---:|---:|---:|---:|
| zxlauncher | False | 71963 | 6307 | 46978 | 1934 |
| zxstore | False | 99787 | 1118 | 4792 | 193 |
| KuSetupWizard | True | 47105 | 4 | 2 | 0 |

## zxlauncher

- APK byte-identical: False
- OEM-owned changed methods: 1934
- Changes matched to important feature keywords: 1893

### Candidate changed OEM methods
- only_new_8052 — com/zeasn/launcher/CustomApplication.java :: AnonymousClass2()
- only_new_8052 — com/zeasn/launcher/CustomApplication.java :: attachBaseContext(android.content.Context context)
- changed_body — com/zeasn/launcher/CustomApplication.java :: createFocusEffect()
- changed_body — com/zeasn/launcher/CustomApplication.java :: createProductFlavors()
- only_old_8054 — com/zeasn/launcher/CustomApplication.java :: customMacPersist()
- only_old_8054 — com/zeasn/launcher/CustomApplication.java :: getCustomMySnControl()
- changed_body — com/zeasn/launcher/CustomApplication.java :: getDeviceType()
- changed_body — com/zeasn/launcher/CustomApplication.java :: getDeviceTypeValue()
- changed_body — com/zeasn/launcher/CustomApplication.java :: getItemDecoration()
- changed_body — com/zeasn/launcher/CustomApplication.java :: getItemPadding()
- changed_body — com/zeasn/launcher/CustomApplication.java :: getLocalBlackAppList()
- only_new_8052 — com/zeasn/launcher/CustomApplication.java :: getTabIndex(com.zeasn.protocol.TabType tabType)
- only_new_8052 — com/zeasn/launcher/CustomApplication.java :: getUpgradeDownloaderPath()
- only_new_8052 — com/zeasn/launcher/CustomApplication.java :: handlerHomeKey()
- changed_body — com/zeasn/launcher/CustomApplication.java :: initADService()
- changed_body — com/zeasn/launcher/CustomApplication.java :: initEvent()
- only_old_8054 — com/zeasn/launcher/CustomApplication.java :: initLocalAppDataProviderExecutorpool()
- changed_body — com/zeasn/launcher/CustomApplication.java :: initTouAd()
- changed_body — com/zeasn/launcher/CustomApplication.java :: initTracker()
- changed_body — com/zeasn/launcher/CustomApplication.java :: initWeather()
- changed_body — com/zeasn/launcher/CustomApplication.java :: onCreate()
- only_new_8052 — com/zeasn/launcher/CustomApplication.java :: onFailed(java.lang.String str)
- only_new_8052 — com/zeasn/launcher/CustomApplication.java :: onReceive(android.content.Context context, android.content.Intent intent)
- only_new_8052 — com/zeasn/launcher/CustomApplication.java :: onSucceed(java.lang.String str)
- only_new_8052 — com/zeasn/launcher/CustomApplication.java :: pluginInit()
- only_new_8052 — com/zeasn/launcher/CustomApplication.java :: pluginUpdate()
- only_old_8054 — com/zeasn/launcher/CustomApplication.java :: presetInstallChange()
- only_new_8052 — com/zeasn/launcher/CustomApplication.java :: registerReceiver(new android.content.BroadcastReceiver()
- changed_body — com/zeasn/launcher/CustomApplication.java :: run()
- only_new_8052 — com/zeasn/launcher/CustomApplication.java :: saveDataToSpTag()
- only_new_8052 — com/zeasn/launcher/CustomApplication.java :: setData(java.util.Map<java.lang.String, java.lang.Object> map)
- only_new_8052 — com/zeasn/launcher/CustomApplication.java :: setMsg(java.lang.String str)
- only_new_8052 — com/zeasn/launcher/R.java :: R()
- only_new_8052 — com/zeasn/launcher/R.java :: anim()
- only_new_8052 — com/zeasn/launcher/R.java :: animator()
- only_new_8052 — com/zeasn/launcher/R.java :: array()
- only_new_8052 — com/zeasn/launcher/R.java :: attr()
- only_new_8052 — com/zeasn/launcher/R.java :: bool()
- only_new_8052 — com/zeasn/launcher/R.java :: color()
- only_new_8052 — com/zeasn/launcher/R.java :: dimen()
- only_new_8052 — com/zeasn/launcher/R.java :: drawable()
- only_new_8052 — com/zeasn/launcher/R.java :: font()
- only_new_8052 — com/zeasn/launcher/R.java :: fraction()
- only_new_8052 — com/zeasn/launcher/R.java :: id()
- only_new_8052 — com/zeasn/launcher/R.java :: integer()
- only_new_8052 — com/zeasn/launcher/R.java :: interpolator()
- only_new_8052 — com/zeasn/launcher/R.java :: layout()
- only_new_8052 — com/zeasn/launcher/R.java :: mipmap()
- only_new_8052 — com/zeasn/launcher/R.java :: plurals()
- only_new_8052 — com/zeasn/launcher/R.java :: raw()
- only_new_8052 — com/zeasn/launcher/R.java :: string()
- only_new_8052 — com/zeasn/launcher/R.java :: style()
- only_new_8052 — com/zeasn/launcher/R.java :: styleable()
- only_new_8052 — com/zeasn/launcher/R.java :: transition()
- only_new_8052 — com/zeasn/launcher/R.java :: xml()
- only_new_8052 — com/zeasn/launcher/adapter/AppsAllTitleAdapter.java :: AppsAllTitleAdapter(android.content.Context context, androidx.leanback.widget.VerticalGridView verticalGridView)
- only_new_8052 — com/zeasn/launcher/adapter/AppsAllTitleAdapter.java :: onBind(final com.zeasn.launcher.model.ViewHolder viewHolder, java.lang.Object obj, final int i)
- only_new_8052 — com/zeasn/launcher/adapter/AppsAllTitleAdapter.java :: onFocusChange(android.view.View view, boolean z)
- only_new_8052 — com/zeasn/launcher/adapter/AppsAllTitleAdapter.java :: run()
- only_new_8052 — com/zeasn/launcher/adapter/AppsAllTitleAdapter.java :: setCategory(com.zeasn.launcher.model.ViewHolder viewHolder, java.lang.Object obj)
- only_new_8052 — com/zeasn/launcher/adapter/AppsAllTitleAdapter.java :: setOnItemClickListener(com.zeasn.launcher.adapter.AppsAllTitleAdapter.OnItemClickListener onItemClickListener)
- only_new_8052 — com/zeasn/launcher/adapter/BaseRecyclerAdapter.java :: BaseRecyclerAdapter(android.content.Context context, java.util.List<T> list)
- only_new_8052 — com/zeasn/launcher/adapter/BaseRecyclerAdapter.java :: clear()
- only_new_8052 — com/zeasn/launcher/adapter/BaseRecyclerAdapter.java :: getCount()
- only_new_8052 — com/zeasn/launcher/adapter/BaseRecyclerAdapter.java :: getItemCount()

## zxstore

- APK byte-identical: False
- OEM-owned changed methods: 193
- Changes matched to important feature keywords: 60

### Candidate changed OEM methods
- changed_body — com/zeasn/utils/NetWorkUtils.java :: getNetWorkType(android.content.Context context)
- changed_body — zeasn/open/technical/tv/store/CustomApplication.java :: localChagedBroadcast()
- changed_body — zeasn/open/technical/tv/store/CustomApplication.java :: registerReceiver(new android.content.BroadcastReceiver()
- only_old_8054 — zeasn/open/technical/tv/store/app/AppDetailBoner.java :: getInstallFailReason(int i, java.lang.String str)
- only_new_8052 — zeasn/open/technical/tv/store/app/AppDetailBoner.java :: onInstallFailed(java.lang.String str, boolean z, int i)
- only_old_8054 — zeasn/open/technical/tv/store/app/AppDetailBoner.java :: onInstallFailed(java.lang.String str, boolean z, int i, int i2, java.lang.String str2)
- only_new_8052 — zeasn/open/technical/tv/store/app/BonerPrivoder.java :: onInstallFailed(java.lang.String str, boolean z2, int i)
- only_old_8054 — zeasn/open/technical/tv/store/app/BonerPrivoder.java :: onInstallFailed(java.lang.String str, boolean z2, int i, int i2, java.lang.String str2)
- changed_body — zeasn/open/technical/tv/store/app/BonerPrivoder.java :: slientInstall(boolean z, android.content.Context context, final com.lzy.okserver.download.DownloadInfo downloadInfo)
- changed_body — zeasn/open/technical/tv/store/app/InstallRunnable.java :: AndroidPAppInstaller()
- changed_body — zeasn/open/technical/tv/store/app/InstallRunnable.java :: InstallRunnable(android.content.Context context, java.lang.String str, java.lang.String str2, final androidx.lifecycle.Observer<java.lang.Boolean> observer)
- only_old_8054 — zeasn/open/technical/tv/store/app/InstallRunnable.java :: getInstallFailReason(int i, java.lang.String str)
- only_old_8054 — zeasn/open/technical/tv/store/app/InstallRunnable.java :: notifyInstallState(int i, java.lang.String str)
- changed_body — zeasn/open/technical/tv/store/app/InstallRunnable.java :: onCreated(int i)
- only_old_8054 — zeasn/open/technical/tv/store/app/InstallRunnable.java :: onReceive(android.content.Context context, android.content.Intent intent)
- changed_body — zeasn/open/technical/tv/store/app/InstallRunnable.java :: run()
- only_old_8054 — zeasn/open/technical/tv/store/app/TouHelperImpl.java :: getBootTouListener()
- only_old_8054 — zeasn/open/technical/tv/store/app/TouHelperImpl.java :: getSettingTouListener()
- only_old_8054 — zeasn/open/technical/tv/store/app/TouHelperImpl.java :: onBootTouDpListResult(java.util.List<com.zeasn.dpapi.bean.Service> list)
- changed_body — zeasn/open/technical/tv/store/app/UpdatedDataProvider.java :: onChanged(com.lzy.okserver.download.DownloadInfo downloadInfo)
- only_old_8054 — zeasn/open/technical/tv/store/ui/AdTouBannerHelperImpl.java :: adBannerDirectionFocusChange(int i, android.view.View view, boolean z)
- only_old_8054 — zeasn/open/technical/tv/store/ui/AdTouBannerHelperImpl.java :: adUpdateBannerAdList(boolean z)
- only_old_8054 — zeasn/open/technical/tv/store/ui/MainActivity.java :: updateBannerWebAdViewData()
- only_old_8054 — zeasn/open/technical/tv/store/ui/SettingTouActivity.java :: getSettingOptions()
- changed_body — zeasn/open/technical/tv/store/ui/SettingTouActivity.java :: initView(android.os.Bundle bundle)
- only_old_8054 — zeasn/open/technical/tv/store/ui/SettingTouActivity.java :: onItemOnclick(android.view.View view, android.view.View view2, int i, java.lang.Object obj)
- only_old_8054 — zeasn/open/technical/tv/store/ui/SettingTouActivity_ViewBinding.java :: SettingTouActivity_ViewBinding(zeasn.open.technical.tv.store.ui.SettingTouActivity settingTouActivity)
- only_old_8054 — zeasn/open/technical/tv/store/ui/SettingTouActivity_ViewBinding.java :: SettingTouActivity_ViewBinding(zeasn.open.technical.tv.store.ui.SettingTouActivity settingTouActivity, android.view.View view)
- only_old_8054 — zeasn/open/technical/tv/store/ui/SettingTouActivity_ViewBinding.java :: unbind()
- changed_body — zeasn/open/technical/tv/store/ui/SettingUpgradeActivity.java :: onDestroy()
- only_new_8052 — zeasn/open/technical/tv/store/ui/dialogbuilder/AuthDialogBuilder.java :: getAppVersionViewId()
- only_new_8052 — zeasn/open/technical/tv/store/ui/dialogbuilder/AuthDialogBuilder.java :: getContentViewId()
- only_new_8052 — zeasn/open/technical/tv/store/ui/dialogbuilder/AuthDialogBuilder.java :: getDPViewId()
- only_new_8052 — zeasn/open/technical/tv/store/ui/dialogbuilder/AuthDialogBuilder.java :: getErrorCode()
- only_new_8052 — zeasn/open/technical/tv/store/ui/dialogbuilder/AuthDialogBuilder.java :: getErrorCodeViewId()
- only_new_8052 — zeasn/open/technical/tv/store/ui/dialogbuilder/AuthDialogBuilder.java :: getLayoutRes()
- only_new_8052 — zeasn/open/technical/tv/store/ui/dialogbuilder/AuthDialogBuilder.java :: getProductViewId()
- only_new_8052 — zeasn/open/technical/tv/store/ui/dialogbuilder/AuthDialogBuilder.java :: getQrcodeViewId()
- only_new_8052 — zeasn/open/technical/tv/store/ui/dialogbuilder/AuthDialogBuilder.java :: getRetryViewId()
- only_new_8052 — zeasn/open/technical/tv/store/ui/dialogbuilder/AuthDialogBuilder.java :: getSNViewId()
- only_new_8052 — zeasn/open/technical/tv/store/ui/dialogbuilder/AuthDialogBuilder.java :: getTerminalTypeViewId()
- only_new_8052 — zeasn/open/technical/tv/store/ui/dialogbuilder/BaseMacAuthDialogBuilder.java :: createQRImage(android.content.Context context, java.lang.String str)
- only_new_8052 — zeasn/open/technical/tv/store/ui/dialogbuilder/BaseMacAuthDialogBuilder.java :: getAppVersionCode(android.content.Context context)
- only_new_8052 — zeasn/open/technical/tv/store/ui/dialogbuilder/BaseMacAuthDialogBuilder.java :: initDialogView(android.app.Dialog dialog)
- only_new_8052 — zeasn/open/technical/tv/store/ui/dialogbuilder/BaseMacAuthDialogBuilder.java :: onClick(android.view.View view2)
- only_new_8052 — zeasn/open/technical/tv/store/ui/dialogbuilder/BaseMacAuthDialogBuilder.java :: retry()
- only_new_8052 — zeasn/open/technical/tv/store/ui/dialogbuilder/BaseMacAuthDialogBuilder.java :: show(android.content.DialogInterface dialogInterface)
- changed_body — zeasn/open/technical/tv/store/ui/dialogbuilder/MacNotAuthDialogBuilder.java :: OnClick(android.view.View view)
- only_old_8054 — zeasn/open/technical/tv/store/ui/dialogbuilder/MacNotAuthDialogBuilder.java :: killProcess()
- only_old_8054 — zeasn/open/technical/tv/store/ui/dialogbuilder/MacNotAuthDialogBuilder.java :: restartAndroid15Plus(android.content.Context context, android.content.ComponentName componentName)
- only_old_8054 — zeasn/open/technical/tv/store/ui/dialogbuilder/MacNotAuthDialogBuilder.java :: restartBelowAndroid15(android.content.Context context, android.content.Intent intent)
- changed_body — zeasn/open/technical/tv/store/ui/dialogbuilder/MacNotAuthDialogBuilder_ViewBinding.java :: MacNotAuthDialogBuilder_ViewBinding(final zeasn.open.technical.tv.store.ui.dialogbuilder.MacNotAuthDialogBuilder macNotAuthDialogBuilder, android.view.View view)
- changed_body — zeasn/open/technical/tv/store/ui/dialogbuilder/MacNotAuthDialogBuilder_ViewBinding.java :: unbind()
- changed_body — zeasn/open/technical/tv/store/ui/dialogbuilder/NetworkWrongDialogBuilder_ViewBinding.java :: NetworkWrongDialogBuilder_ViewBinding(final zeasn.open.technical.tv.store.ui.dialogbuilder.NetworkWrongDialogBuilder networkWrongDialogBuilder, android.view.View view)
- changed_body — zeasn/open/technical/tv/store/ui/dialogbuilder/NetworkWrongDialogBuilder_ViewBinding.java :: unbind()
- changed_body — zeasn/open/technical/tv/store/ui/dialogbuilder/UpdateDialogBuilder.java :: notifyUI()
- only_old_8054 — zeasn/open/technical/tv/store/utils/DownloadUpdateUtil.java :: NetworkChangeReceiver()
- changed_body — zeasn/open/technical/tv/store/utils/DownloadUpdateUtil.java :: onFinish(final com.lzy.okserver.download.DownloadInfo downloadInfo)
- only_new_8052 — zeasn/open/technical/tv/store/utils/DownloadUpdateUtil.java :: onInstallFailed(java.lang.String str, boolean z, int i)
- only_old_8054 — zeasn/open/technical/tv/store/utils/DownloadUpdateUtil.java :: onInstallFailed(java.lang.String str, boolean z, int i, int i2, java.lang.String str2)

## KuSetupWizard

- APK byte-identical: True
- OEM-owned changed methods: 0
- Changes matched to important feature keywords: 0

### Candidate changed OEM methods
- No changed OEM method matched filter. Check full JSON.

## Interpretation

- Most changes in support-library code may be build or decompiler noise; concentrate on app-owned method changes.
- Distinguish executable behavior from manifest/resources, because dex hashes alone cannot capture exported components.
- Before removing launcher/store, test shared install broadcasts, package install flow, HOME fallback and system settings writes.
- Setup wizard package can duplicate settings Java code but still have distinct provisioning manifest and lifecycle.
- No APKs were modified or installed.

