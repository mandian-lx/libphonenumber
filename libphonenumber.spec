%{?_javapackages_macros:%_javapackages_macros}

# FIXME: java package may be spiltted into several packages

# FIXME: required by geocode module
%define _disable_ld_no_undefined 1

%define major 8
%define libname %mklibname phonenumber %{major}
%define devname %mklibname phonenumber -d
%define libname_java	phonenumber-java
%define libname_javadoc	phonenumber-javadoc


Summary:	Library for parsing/formatting/validating all international phone numbers
Name:		libphonenumber
Version:	8.3.3
Release:	1
License:	Apache License and MIT and BSD
Group:		System/Libraries
URL:		https://github.com/googlei18n/%{name}/
Source0:	https://github.com/googlei18n/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
# https://github.com/googlei18n/libphonenumber/issues/1307
# https://github.com/googlei18n/libphonenumber/pull/1090
# https://github.com/gjasny/libphonenumber/commit/45bd90ab3e910a14a82e3889a0b309dd4157a283.patch
Patch0:		%{name}-8.3.3-libdir.patch
Patch1:		%{name}-8.3.3-re2.patch
Patch2:		%{name}-8.3.3-readdir_r.patch
Patch3:		%{name}-8.3.3-tests.patch

# cpp library
BuildRequires:	cmake > 2.8
BuildRequires:	pkgconfig(protobuf) >= 2.4
BuildRequires:	gtest-devel
BuildRequires:	re2-devel
BuildRequires:	pkgconfig(icu-uc) >= 4.4
BuildRequires:	pkgconfig(icu-i18n) >= 4.4
BuildRequires:	boost-devel

# java libraries
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.protobuf:protobuf-java)
BuildRequires:  mvn(commons-fileupload:commons-fileupload)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(commons-lang:commons-lang)
BuildRequires:  mvn(javax.servlet:servlet-api)
BuildRequires:  mvn(junit:junit)
#BuildRequires:  mvn(net.kindleit:maven-gae-plugin)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-release-plugin)
#BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-war-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.codehaus.mojo:exec-maven-plugin)
#BuildRequires:  mvn(org.mortbay.jetty:maven-jetty-plugin)

%description
Google's common Java, C++ and JavaScript library for parsing, formatting,
storing and validating international phone numbers. The Java version is
optimized for running on smartphones, and is used by the Android framework
since 4.0 (Ice Cream Sandwich).

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Library for parsing/formatting/validating all international phone numbers
License:	Apache License
Group:		System/Libraries

%description -n %{libname}
Google's common Java, C++ and JavaScript library for parsing, formatting,
storing and validating international phone numbers. The Java version is
optimized for running on smartphones, and is used by the Android framework
since 4.0 (Ice Cream Sandwich).

This package contains the runtime libraries for C++ users.

%files -n %{libname}
%{_libdir}/lib*.so.*
%doc README.md
%doc AUTHORS
%doc CONTRIBUTORS
%doc LICENSE
%doc LICENSE.Chromium
%doc cpp/LICENSE
%doc cpp/README

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Library for parsing/formatting/validating all international phone numbers
License:	Apache License
Group:		Development/C++
Requires:	pkgconfig(protobuf) >= 2.4
Requires:	boost-devel
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
Google's common Java, C++ and JavaScript library for parsing, formatting,
storing and validating international phone numbers. The Java version is
optimized for running on smartphones, and is used by the Android framework
since 4.0 (Ice Cream Sandwich).

This package contains the include files and the other resources for C++
devlopper.

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%doc README.md
%doc AUTHORS
%doc CONTRIBUTORS
%doc LICENSE
%doc LICENSE.Chromium
%doc cpp/LICENSE
%doc cpp/README

#----------------------------------------------------------------------------

%package java
Summary:	Library for parsing/formatting/validating all international phone numbers
Group:		Development/Java
Requires:	java-headless
Requires:	jpackage-utils

%description java
Google's common Java, C++ and JavaScript library for parsing, formatting,
storing and validating international phone numbers. The Java version is
optimized for running on smartphones, and is used by the Android framework
since 4.0 (Ice Cream Sandwich).

This package contains the runtime libraries for Java users.

%files java -f .mfiles
%doc release_notes.txt
%doc README.md
%doc AUTHORS
%doc CONTRIBUTORS
%doc LICENSE
%doc LICENSE.Chromium

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{libname_javadoc}
BuildArch:	noarch

%description javadoc
API documentation for %{libname_javadoc}.

%files javadoc -f .mfiles-javadoc

#----------------------------------------------------------------------------

%prep
%setup -q
# Delete prebuild JARs and classes
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Apply all patches
%patch0 -p1 -b .orig
%patch1 -p1 -b .re2
%patch2 -p1 -b .readdir_r
%patch3 -p1 -b .tests

# Remove parent
%pom_remove_parent java/pom.xml

# Remove unpackaged plugins
%pom_remove_plugin org.codehaus.mojo:animal-sniffer-maven-plugin java/carrier/pom.xml java/demo/pom.xml java/geocoder/pom.xml
%pom_remove_plugin org.codehaus.mojo:animal-sniffer-maven-plugin java/libphonenumber/pom.xml

# Fix jar-not-indexed warning
%pom_add_plugin :maven-jar-plugin java/pom.xml "
<configuration>
	<archive>
		<index>true</index>
	</archive>
</configuration>"

%pom_add_plugin :maven-jar-plugin tools/java/pom.xml "
<configuration>
	<archive>
		<index>true</index>
	</archive>
</configuration>"

# Fix class-path-in-manifest warning
%pom_xpath_remove "pom:project/pom:build/pom:plugins/pom:plugin[pom:artifactId[./text()='maven-jar-plugin']]/pom:configuration/pom:archive/pom:manifest/pom:addClasspath" tools/java/cpp-build/pom.xml

# set the right name to fit the packaging guidelines
%mvn_file ":{*}" %{name}/@1 @1

%build
# c++ library
pushd cpp
%cmake -DUSE_RE2:BOOL=ON
%make phonenumber phonenumber-shared 
popd

# java library
%mvn_build 

%install
# c++ library
%make_install -C cpp/build 

# java library
%mvn_install

%check
# % make -C cpp/build test

