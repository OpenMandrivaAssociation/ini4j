# Prevent brp-java-repack-jars from being run.
%global __jar_repack %{nil}

%global servlet_jar %{_javadir}/servlet.jar
%global jetty_jar %{_javadir}/jetty/jetty.jar

Name:           ini4j
Version:        0.4.1
Release:        %mkrel 3
Summary:        Java API for handling files in Windows .ini format

Group:          Development/Java
License:        ASL 2.0
URL:            http://www.ini4j.org/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.zip
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
Source2:        %{name}-%{version}-build.xml

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

# See http://ini4j.sourceforge.net/dependencies.html
BuildRequires:  jpackage-utils
BuildRequires:  ant
BuildRequires:  java-devel >= 1.6.0
BuildRequires:  tomcat5-servlet-2.4-api >= 5.5
BuildRequires:  jetty5 >= 4.2.2
BuildRequires:  java-rpmbuild >= 0:1.5.32

Requires:       jpackage-utils
Requires:       java >= 1.6.0
Requires:       tomcat5-servlet-2.4-api >= 5.5

%description
The [ini4j] is a simple Java API for handling configuration files in Windows 
.ini format. Additionally, the library includes Java Preferences API 
implementation based on the .ini file.

%package javadoc
Summary:        Javadocs for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep

%setup -q

cp -a %{SOURCE1} ./LICENSE-2.0.txt
cp -a %{SOURCE2} ./build.xml

find . -type f \( -iname "*.jar" -o -iname "*.class" \) | xargs -t %{__rm} -f

# remove test sources
%{__rm} -rf src/test
# remove site sources
%{__rm} -rf src/site

%build

%ant -Dbuild.servlet.jar=%{servlet_jar} -Dbuild.jetty.jar=%{jetty_jar} build javadoc

%install
%{__rm} -rf %{buildroot}

# JAR
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -p dist/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && %{__ln_s} %{name}-%{version}.jar %{name}.jar)

# Javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}
%{__cp} -rp build/doc/api/* %{buildroot}%{_javadocdir}/%{name}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/*
%doc LICENSE-2.0.txt src/main/java/org/ini4j/package.html

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}
