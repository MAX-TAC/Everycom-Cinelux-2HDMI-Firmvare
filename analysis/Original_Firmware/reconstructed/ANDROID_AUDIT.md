# CineLux firmware / Android partitions

Reconstructed and analyzed in read-only form, not flashed.

## Logical partitions

| Partition | Bytes | Format |
|---|---:|---|
| product_a.img | 77152256 | EROFS filesystem, compat: SB_CHKSUM MTIME, blocksize=12, exslots=0, uuid=FBF3C5B1-D809-EE55-8100-1C3 |
| system_a.img | 866844672 | EROFS filesystem, compat: SB_CHKSUM MTIME, blocksize=12, exslots=0, uuid=7BEE08A9-2373-C154-A38A-3AD |
| system_ext_a.img | 87273472 | EROFS filesystem, compat: SB_CHKSUM MTIME, blocksize=12, exslots=0, uuid=A496D428-394B-3C58-BFDC-076 |
| vendor_a.img | 262610944 | EROFS filesystem, compat: SB_CHKSUM MTIME, blocksize=12, exslots=0, uuid=DBB3D2FF-C28D-5757-B7E5-650 |

## Build properties

### system_a.img

~~~
ro.build.version.sdk=33
ro.build.version.release=13
ro.build.version.security_patch=2026-04-05
ro.build.type=userdebug
~~~
### vendor_a.img

~~~
ro.vendor.build.fingerprint=MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/suhaixiong09300739:userdebug/test-keys
ro.product.board=mt5873_cd
ro.board.platform=mt5873
ro.product.model=Projetor
~~~

## System app directories
### product_a.img
app: Camera2, LatinIME, ModuleMetadata, VendorDisclaimer, WallpaperPicker, webview
### system_a.img
system/app: BasicDreams, CertInstaller, CompanionDeviceManager, CtsShimPrebuilt, ExtShared, FTAirplayWireless, HTMLViewer, KeyChain, KuSettings, KuSetupWizard, KuSourceRJ, PacProcessor, PlatformCaptivePortalLogin, PrintSpooler, RJBluetoothSpeaker, RuiAutoFocus, SecureElement, TrdDreamPic, TrdFactoryTest, WallpaperBackup, trdservice, zxlauncher, zxstore
system/priv-app: BackupRestoreConfirmation, CalendarProvider, ContactsProvider, CtsShimPrivPrebuilt, DownloadProvider, DynamicSystemInstallationService, ExternalStorageProvider, FusedLocation, InProcessNetworkStack, InputDevices, KeystoneCorrection, LocalTransport, MediaProviderLegacy, PackageInstaller, ProxyHandler, RuiYunOta, SettingsProvider, SharedStorageBackup, Shell, SoundPicker, StatementService, TvProvider, UserDictionaryProvider, VpnDialogs
### system_ext_a.img
app: AutoPair, Factory, TvFrameworkPackageStubs, WFDSinkTest
priv-app: LiveTV, MtkNetworkMonitorService, MtkTvInput, MultiMediaPlayer, RemoteProvisioner, RetailDisplay, SystemUI, TvServices, TvSettingsPlus
### vendor_a.img
priv-app: trdmiddle

## Declared HALs
### system_ext_a.img

### vendor_a.img
IAllocator, IAudioCapture, IBluetoothAudioProviderFactory, IBluetoothHci, ICameraProvider, ICodec2InfoService, IComponentStore, IComposer, IDevicesFactory, IEffectsFactory, IExternalbuffer, IGatekeeper, IHCmpb, IHdmiCec, IImgDisp, IImgHwDec, IInterTunnel, IMapper, IMmDisp, IMtkCalman, IMtkDmCommon, IMtkMediaPluginService, IMtkPhotoService, IMtkRm, IMtkTvApi, IMtkTvApiBroadcast, IMtkTvApiCI, IMtkTvApiCec, IMtkTvApiChannelList, IMtkTvApiConfig, IMtkTvApiCustom, IMtkTvApiEvent, IMtkTvApiInputSrc, IMtkTvApiMultiview, IMtkTvApiPvrbrowser, IMtkTvApiRating, IMtkTvApiRecord, IMtkTvApiScan, IMtkTvApiTime, IMtkTvApiTimeshift, IMtkTvFApiAudio, IMtkTvFApiCustom, IMtkTvFApiDisplay, IMtkTvFApiDisplayTest, IMtkTvFApiInformation, IMtkTvFApiInputSource, IMtkTvFApiManager, IMtkTvFApiNetwork, IMtkTvFApiPeripheral, IMtkTvFApiSystem, IMtkTvFApiTv, IMtkTvVoc, IMtkVssService, IMtkWifiDisplay, INetworkProxy, IOmx, IOmxStore, IScreenCapture, IScreenEncoder, ISensors, ITvInput, android.hardware.audio, android.hardware.audio.effect, android.hardware.bluetooth, android.hardware.bluetooth.audio, android.hardware.camera.provider, android.hardware.gatekeeper, android.hardware.graphics.allocator, android.hardware.graphics.composer, android.hardware.graphics.mapper, android.hardware.media.c2, android.hardware.media.omx, android.hardware.sensors, android.hardware.tv.cec, android.hardware.tv.input, mstar.hardware.imgdisp, mstar.hardware.imghwdec, mstar.hardware.intertunnel, mstar.hardware.mmdisp, vendor.mediatek.api.mtktvapi, vendor.mediatek.custom.mtktvapicustom, vendor.mediatek.graphics.externalbuffer, vendor.mediatek.hardware.c2.info, vendor.mediatek.hardware.tv.networkproxy, vendor.mediatek.tv.Mm.Mm.mtktvfapicustom, vendor.mediatek.tv.cmpb, vendor.mediatek.tv.mtkcalman, vendor.mediatek.tv.mtkdmservice, vendor.mediatek.tv.mtkmtalservice, vendor.mediatek.tv.mtkrm, vendor.mediatek.tv.mtktvfactory, vendor.mediatek.tv.mtktvvoc, vendor.mediatek.tv.screenrecord, vendor.mediatek.wifidisplay
