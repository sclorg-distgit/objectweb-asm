# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%{?scl:%scl_package objectweb-asm}
%{!?scl:%global pkg_name %{name}}

%{?thermostat_find_provides_and_requires}

Name:           %{?scl_prefix}objectweb-asm
Version:        3.3.1
Release:        8.4%{?dist}
Epoch:          0
Summary:        A code manipulation tool to implement adaptable systems
License:        BSD
URL:            http://asm.objectweb.org/
Source0:        http://download.forge.objectweb.org/asm/asm-3.3.1.tar.gz

BuildArch:      noarch

BuildRequires:  maven30-ant
BuildRequires:  maven30-maven-local

%description
ASM is an all purpose Java bytecode manipulation and analysis
framework.  It can be used to modify existing classes or dynamically
generate classes, directly in binary form.  Provided common
transformations and analysis algorithms allow to easily assemble
custom complex transformations and code analysis tools.

%package        javadoc
Summary:        API documentation for %{name}

%description    javadoc
This package provides %{summary}.

%prep
%{?scl:scl enable maven30 %{scl} - << "EOF"}
%setup -q -n asm-%{version}
find -name *.jar -delete
%mvn_alias :asm-all org.eclipse.jetty.orbit:org.objectweb.asm

sed -i /Class-path/d archive/asm-xml.xml
%{?scl:EOF}

%build
%{?scl:scl enable maven30 %{scl} - << "EOF"}
%ant -Dobjectweb.ant.tasks.path= jar jdoc
%{?scl:EOF}

%install
%{?scl:scl enable maven30 %{scl} - << "EOF"}
for m in asm asm-analysis asm-commons asm-tree asm-util asm-xml all/asm-all; do
    %mvn_artifact output/dist/lib/${m}-%{version}.pom \
                  output/dist/lib/${m}-%{version}.jar
done
%mvn_install -J output/dist/doc/javadoc/user
# Own the objectweb-asm directory in order to avoid it sticking
# around after removal
install -d -m 755 %{buildroot}%{_javadir}/%{pkg_name}
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE.txt README.txt
# Own the objectweb-asm directory in order to avoid it sticking
# around after removal
%dir %{_javadir}/%{pkg_name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Fri Jun 20 2014 Severin Gehwolf <sgehwolf@redhat.com> - 0:3.3.1-8.4
- Own objectweb-asm directory.

* Tue Jun 17 2014 Severin Gehwolf <sgehwolf@redhat.com> - 0:3.3.1-8.3
- Rebuild against maven30 collection.

* Mon Jan 20 2014 Severin Gehwolf <sgehwolf@redhat.com> - 0:3.3.1-8.2
- Rebuild in order to fix osgi()-style provides.
- Resolves: RHBZ#1054813

* Mon Nov 18 2013 Michal Srb <msrb@redhat.com> - 0:3.3.1-8.1
- Enable SCL for thermostat

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.3.1-8
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Mar  6 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.3.1-7
- Make jetty orbit depmap point to asm-all jar
- Resolves: rhbz#917625

* Mon Mar  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.3.1-6
- Add depmap for org.eclipse.jetty.orbit
- Resolves: rhbz#917625

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 16 2011 Alexander Kurtakov <akurtako@redhat.com> 0:3.3.1-2
- Use poms produced by the build not foreign ones.
- Adpat to current guidelines.

* Mon Apr 04 2011 Chris Aniszczyk <zx@redhat.com> 0:3.3.1
- Upgrade to 3.3.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 13 2010 Orion Poplawski <orion@cora.nwra.com>  0:3.2.1-2
- Change depmap parent id to asm (bug #606659)

* Thu Apr 15 2010 Fernando Nasser <fnasser@redhat.com> 0:3.2.1
- Upgrade to 3.2

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.1-7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.1-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 23 2008 David Walluck <dwalluck@redhat.com> 0:3.1-5.1
- build for Fedora

* Tue Oct 23 2008 David Walluck <dwalluck@redhat.com> 0:3.1-5
- add OSGi manifest (Alexander Kurtakov)

* Mon Oct 20 2008 David Walluck <dwalluck@redhat.com> 0:3.1-4
- remove Class-Path from MANIFEST.MF
- add unversioned javadoc symlink
- remove javadoc scriptlets
- fix directory ownership
- remove build requirement on dos2unix

* Fri Feb 08 2008 Ralph Apel <r.apel@r-apel.de> - 0:3.1-3jpp
- Add poms and depmap frags with groupId of org.objectweb.asm !
- Add asm-all.jar 
- Add -javadoc Requires post and postun
- Restore Vendor, Distribution

* Thu Nov 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.1-2jpp
- Fix EOL of txt files
- Add dependency on jaxp 

* Thu Nov 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.1-1jpp
- Upgrade to 3.1

* Wed Aug 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.0-1jpp
- Upgrade to 3.0
- Rename to include objectweb- prefix as requested by ObjectWeb

* Thu Jan 05 2006 Fernando Nasser <fnasser@redhat.com> - 0:2.1-2jpp
- First JPP 1.7 build

* Thu Oct 06 2005 Ralph Apel <r.apel at r-apel.de> 0:2.1-1jpp
- Upgrade to 2.1

* Fri Mar 11 2005 Sebastiano Vigna <vigna at acm.org> 0:2.0.RC1-1jpp
- First release of the 2.0 line.
