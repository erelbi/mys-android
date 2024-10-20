[app]
title = MYS
package.name = mysapp
package.domain = org.test.magazayonetim
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,xml
version = 0.1
requirements = python3,kivy,android,kivymd
orientation = portrait
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 34
android.minapi = 21
android.ndk = 25b
#android.sdk = 34
android.enable_androidx = True
android.gradle_dependencies = androidx.core:core:1.6.0, androidx.work:work-runtime:2.7.0
p4a.branch = master
android.gradle_version = 7.3.0
source.exclude_dirs = venv, .buildozer , .github, .vscode, img,bin
source.exclude_patterns = license,images/*/*.jpg,*.pyc,*.pyo
android.add_xml_to_zip = AndroidManifest.xml,res/xml/file_paths.xml
android.manifest = AndroidManifest.xml
icon.filename = mys.png
presplash.filename = splash.png
android.meta_data = android.support.FILE_PROVIDER_PATHS=@res/xml/file_paths.xml






