# TODO:
# - support for Oracle and Sybase
#
%include	/usr/lib/rpm/macros.php
Summary:	The common Horde Framework for all Horde modules
Summary(es):	Elementos básicos do Horde Web Application Suite
Summary(pl):	Wspólny szkielet Horde do wszystkich modu³ów Horde
Summary(pt_BR):	Componentes comuns do Horde usados por todos os módulos
Name:		horde
Version:	3.0.3
Release:	2.11
License:	LGPL
Vendor:		The Horde Project
Group:		Development/Languages/PHP
Source0:	ftp://ftp.horde.org/pub/horde/%{name}-%{version}.tar.gz
# Source0-md5:	96a4c9fb2047987164a3981a31667ef2
Source1:	%{name}.conf
Patch0:		%{name}-path.patch
URL:		http://www.horde.org/
BuildRequires:	rpmbuild(macros) >= 1.177
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
PreReq:		apache-mod_dir >= 1.3.22
Requires(triggerpostun):	grep
Requires(triggerpostun):	sed >= 4.0
Requires:	apache >= 1.3.33-3
Requires:	php >= 4.1.0
Requires:	php-gettext >= 4.1.0
Requires:	php-imap >= 4.1.0
Requires:	php-mcrypt >= 4.1.0
Requires:	php-pear-PEAR
Requires:	php-pear-Log
Requires:	php-pcre >= 4.1.0
Requires:	php-posix >= 4.1.0
Requires:	php-session >= 4.1.0
Requires:	php-xml >= 4.1.0
Obsoletes:	horde-mysql
Obsoletes:	horde-pgsql
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'pear(XML/WBXML.*)' 'pear(Horde.*)' 'pear(Text/.*)' 'pear(Net/IMSP.*)'

%define		_sysconfdir	/etc/horde.org
%define		hordedir	/usr/share/horde
%define		_apache1dir	/etc/apache
%define		_apache2dir	/etc/httpd

%define		_php5		%(rpm -q php | awk -F- '{print $2}' | awk -F. '{print $1}')
%if "%{_php5}" == "5"
Requires:	php-dom
%else
Requires:	php-domxml
%endif

%description
The Horde Framework provides a common structure and interface for
Horde modules (such as IMP, a web-based mail program). This RPM is
required for all other Horde module RPMS.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with Horde and its modules) please visit <http://www.horde.org/>.

%description -l pl
Szkielet Horde dostarcza wspóln± strukturê oraz interfejs dla modu³ów
Horde, takich jak IMP (obs³uga poczty poprzez WWW). Ten pakiet jest
wymagany dla wszystkich innych modu³ów Horde.

Projekt Horde tworzy aplikacje w PHP i dostarcza je na licencji GNU
Public License. Je¿eli chcesz siê dowiedzieæ czego¶ wiêcej (tak¿e help
do IMP-a) zajrzyj na stronê <http://www.horde.org/>.

%description -l pt_BR
Este pacote provê uma interface e estrutura comuns para os módulos
Horde (como IMP, um programa de webmail) e é requerido por todos os
outros módulos Horde.

O Projeto Horde é constituído por diversos aplicativos web escritos em
PHP, todos liberados sob a GPL. Para mais informações (incluindo ajuda
com relação ao Horde e seus módulos), por favor visite
<http://www.horde.org/>.

%prep
%setup -q
%patch0 -p1

# Described in documentation as dangerous file...
rm test.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/horde \
	$RPM_BUILD_ROOT%{hordedir}/{admin,js,lib,locale,services} \
	$RPM_BUILD_ROOT%{hordedir}/{templates,themes,util} \

cp -pR scripts docs
cp -pR	*.php			$RPM_BUILD_ROOT%{hordedir}

for i in admin js lib locale services templates themes util; do
	cp -pR $i/*		$RPM_BUILD_ROOT%{hordedir}/$i
done

for i in lib locale templates; do
	cp -p $i/.htaccess	$RPM_BUILD_ROOT%{hordedir}/$i
done

for i in config/*.php.dist; do
	cp -p $i $RPM_BUILD_ROOT%{_sysconfdir}/horde/$(basename $i .dist)
done

cp -p  config/*.xml		$RPM_BUILD_ROOT%{_sysconfdir}/horde

install	%{SOURCE1}		$RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
ln -fs %{_sysconfdir}/%{name} 	$RPM_BUILD_ROOT%{hordedir}/config

%clean
rm -rf $RPM_BUILD_ROOT

%post
# apache1
if [ -d %{_apache1dir}/conf.d ]; then
	ln -sf %{_sysconfdir}/apache.conf %{_apache1dir}/conf.d/99_%{name}.conf
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi
# apache2
if [ -d %{_apache2dir}/httpd.conf ]; then
	ln -sf %{_sysconfdir}/apache.conf %{_apache2dir}/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%banner %{name} -e <<EOF
IMPORTANT:
If you are installing for the first time, You must now
create the Horde database tables. Look into directory
/usr/share/doc/%{name}-%{version}/scripts/sql
to find out how to do this for your database.
EOF

%preun
if [ "$1" = "0" ]; then
	# apache1
	if [ -d %{_apache1dir}/conf.d ]; then
		rm -f %{_apache1dir}/conf.d/99_%{name}.conf
		if [ -f /var/lock/subsys/apache ]; then
			/etc/rc.d/init.d/apache restart 1>&2
		fi
	fi
	# apache2
	if [ -d %{_apache2dir}/httpd.conf ]; then
		rm -f %{_apache2dir}/httpd.conf/99_%{name}.conf
		if [ -f /var/lock/subsys/httpd ]; then
			/etc/rc.d/init.d/httpd restart 1>&2
		fi
	fi
fi

%triggerpostun -- horde <= 2.2.7-2
for i in horde.php html.php lang.php mime_drivers.php mime_mapping.php motd.php prefs.php registry.php; do
	if [ -f /home/services/httpd/html/horde/config/$i.rpmsave ]; then
		cp -f %{_sysconfdir}/%{name}/$i %{_sysconfdir}/%{name}/$i.rpmnew
		mv -f /home/services/httpd/html/horde/config/$i.rpmsave %{_sysconfdir}/%{name}/$i
	fi
done

%triggerpostun -- horde <= 3.0.3-2
# apache1 confdir
if [ -f /etc/apache/apache.conf ] && grep -q '^Include conf\.d' /etc/apache/apache.conf; then
	sed -i -e '
		/^Include.*mod_horde\.conf/d
	' /etc/apache/apache.conf
else
	# they're still using old apache.conf
	sed -i -e '
		s,^Include.*mod_horde\.conf,Include %{_sysconfdir}/conf.d/*_mod_horde.conf,
	' /etc/apache/apache.conf
fi

if [ -f %{_apache1dir}/horde.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/apache.conf{,.rpmnew}
	mv -f %{_apache1dir}/horde.conf.rpmsave %{_sysconfdir}/apache.conf
fi

if [ -f %{_apache2dir}/horde.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/apache.conf{,.rpmnew}
	mv -f %{_apache2dir}/horde.conf.rpmsave %{_sysconfdir}/apache.conf
fi

if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%files
%defattr(644,root,root,755)
%doc README docs/{HACKING,CONTRIBUTING,CODING_STANDARDS,CHANGES,INSTALL,scripts}
%dir %{hordedir}
%dir %{_sysconfdir}
%{hordedir}/*.php
%{hordedir}/admin
%{hordedir}/config
%{hordedir}/js
%{hordedir}/lib
%{hordedir}/locale
%{hordedir}/services
%{hordedir}/templates
%{hordedir}/themes
%{hordedir}/util
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache.conf
%attr(770,root,http) %dir %{_sysconfdir}/horde
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/horde/*.php
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/horde/*.xml
