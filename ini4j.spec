# Prevent brp-java-repack-jars from being run.
%global __jar_repack %{nil}

%global servlet_jar %{_javadir}/servlet.jar
%global jetty_jar %{_javadir}/jetty/jetty.jar

Name:           ini4j
Version:        0.4.1
Release:        4
Summary:        Java API for handling files in Windows .ini format

Group:          Development/Java
License:        ASL 2.0
URL:            https://www.ini4j.org/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.zip
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
Source2:        %{name}-%{version}-build.xml

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

# JAR
%{__mkdir_p} %{buildroot}%{_javadir}
cp -p dist/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && %{__ln_s} %{name}-%{version}.jar %{name}.jar)

# Javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}
cp -rp build/doc/api/* %{buildroot}%{_javadocdir}/%{name}

%files
%defattr(-,root,root,-)
%{_javadir}/*
%doc LICENSE-2.0.txt src/main/java/org/ini4j/package.html

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}


%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4.1-3mdv2011.0
+ Revision: 619629
- the mass rebuild of 2010.0 packages

* Fri Sep 25 2009 Jaroslav Tulach <jtulach@mandriva.org> 0.4.1-2mdv2010.0
+ Revision: 448936
- Upgrading to 0.4.1 version

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 0:0.2.6-4.0.2mdv2010.0
+ Revision: 429511
- rebuild

* Mon Feb 18 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:0.2.6-4.0.1mdv2008.1
+ Revision: 171024
- spec cleanup

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:0.2.6-4mdv2008.1
+ Revision: 120893
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Mon Dec 10 2007 Jaroslav Tulach <jtulach@mandriva.org> 0:0.2.6-3mdv2008.1
+ Revision: 116877
- Fixing broken link from ini4j.jar

  + Thierry Vignaud <tv@mandriva.org>
    - better summary

* Wed Dec 05 2007 Jaroslav Tulach <jtulach@mandriva.org> 0:0.2.6-2mdv2008.1
+ Revision: 115624
- Creating generic ini4j.jar link to actual version of the JAR file

* Fri Nov 30 2007 Jaroslav Tulach <jtulach@mandriva.org> 0:0.2.6-1mdv2008.1
+ Revision: 114099
- According to template standard file, javadoc belongs to Dev/Java group
- Build also contains junit tests and thus needs a dependency on ant-junit
- Inproper specification of build root
- The build needs proper dependency on ant-nodeps
- import ini4j


