# TODO:
# - support for Oracle and Sybase
# - make default install secure. so that it doesn't auto auth you to
#   administrator. ip restriction in apache? any better ideas?
# - remove config/ (and others in apache.conf) from document root, so
#   apache deny from all not needed.
# - put docs/CREDITS to package, rather in doc (so installations with
#   --excludedocs have functional horde?)
#
%include	/usr/lib/rpm/macros.php
Summary:	The common Horde Framework for all Horde modules
Summary(es):	Elementos básicos do Horde Web Application Suite
Summary(pl):	Wspólny szkielet Horde do wszystkich modu³ów Horde
Summary(pt_BR):	Componentes comuns do Horde usados por todos os módulos
Name:		horde
Version:	3.0.3
Release:	2.36
License:	LGPL
Vendor:		The Horde Project
Group:		Development/Languages/PHP
Source0:	ftp://ftp.horde.org/pub/horde/%{name}-%{version}.tar.gz
# Source0-md5:	96a4c9fb2047987164a3981a31667ef2
Source1:	%{name}.conf
Patch0:		%{name}-path.patch
Patch1:		%{name}-shell.disabled.patch
Patch2:		%{name}-util-h3.patch
URL:		http://www.horde.org/
BuildRequires:	rpmbuild(macros) >= 1.177
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
Requires(triggerpostun):	grep
Requires(triggerpostun):	sed >= 4.0
Requires:	apache >= 1.3.33-3
Requires:	apache(mod_dir) >= 1.3.22
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
Requires:	php-zlib >= 4.1.0
Obsoletes:	horde-mysql
Obsoletes:	horde-pgsql
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq	'pear(XML/WBXML.*)' 'pear(Horde.*)' 'pear(Text/.*)' 'pear(Net/IMSP.*)'

%define		hordedir	/usr/share/horde
%define		_sysconfdir	/etc/horde.org
%define		_appdir		%{hordedir}
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
%patch1 -p1
%patch2 -p1

# Described in documentation as dangerous file...
rm test.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name} \
	$RPM_BUILD_ROOT%{_appdir}/{admin,js,services} \
	$RPM_BUILD_ROOT%{_appdir}/{docs,lib,locale,templates,themes} \
	$RPM_BUILD_ROOT/var/log/%{name}

cp -pR *.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.php.dist; do
	cp -p $i $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/$(basename $i .dist)
done
sed -e '
    s,/tmp/horde.log,/var/log/%{name}/%{name}.log,
'< config/conf.xml > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.xml
> $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php.bak

cp -pR  admin/*                 $RPM_BUILD_ROOT%{_appdir}/admin
cp -pR  js/*                    $RPM_BUILD_ROOT%{_appdir}/js
cp -pR  services/*              $RPM_BUILD_ROOT%{_appdir}/services

cp -pR  lib/*                   $RPM_BUILD_ROOT%{_appdir}/lib
cp -pR  locale/*                $RPM_BUILD_ROOT%{_appdir}/locale
cp -pR  templates/*             $RPM_BUILD_ROOT%{_appdir}/templates
cp -pR  themes/*                $RPM_BUILD_ROOT%{_appdir}/themes

ln -s %{_sysconfdir}/%{name} 	$RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_defaultdocdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs

install %{SOURCE1} 		$RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf

> $RPM_BUILD_ROOT/var/log/%{name}/%{name}.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/%{name}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/%{name}/conf.php.bak
fi

# apache1
if [ -d %{_apache1dir}/conf.d ]; then
	ln -sf %{_sysconfdir}/apache-%{name}.conf %{_apache1dir}/conf.d/99_%{name}.conf
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi
# apache2
if [ -d %{_apache2dir}/httpd.conf ]; then
	ln -sf %{_sysconfdir}/apache-%{name}.conf %{_apache2dir}/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

if [ "$1" = 1 ]; then
# put this message all properly together.
%banner %{name} -e <<EOF

IMPORTANT:
If You are installing horde for the first time, You must
create the Horde database tables. Look into directory
%{_defaultdocdir}/%{name}-%{version}/scripts/sql
to find out how to do this for Your database.

Depending on authorization You choose,
You need to install php-ldap package and setup ldap schema from
%{_defaultdocdir}/%{name}-%{version}/scripts/ldap.

NOTE: You don't need SQL database, if you use LDAP for
authorization.

EOF
# '

fi

%postun
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

%triggerpostun -- horde <= 3.0.3-2.23
# apache1 confdir
if [ -f /etc/apache/apache.conf ]; then
	if grep -q '^Include conf\.d' /etc/apache/apache.conf; then
		sed -i -e '
			/^Include.*mod_horde\.conf/d
		' /etc/apache/apache.conf
	else
		# they're still using old apache.conf
		sed -i -e '
			s,^Include.*mod_horde\.conf,Include %{_sysconfdir}/conf.d/*_mod_horde.conf,
		' /etc/apache/apache.conf
	fi
fi

if [ -f %{_apache1dir}/horde.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/apache-%{name}.conf{,.rpmnew}
	mv -f %{_apache1dir}/horde.conf.rpmsave %{_sysconfdir}/apache-%{name}.conf
fi

if [ -f %{_apache2dir}/horde.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/apache-%{name}.conf{,.rpmnew}
	mv -f %{_apache2dir}/horde.conf.rpmsave %{_sysconfdir}/apache-%{name}.conf
fi

# unified location
if [ -f %{_sysconfdir}/apache.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/apache-%{name}.conf{,.rpmnew}
	mv -f %{_sysconfdir}/apache.conf.rpmsave %{_sysconfdir}/apache-%{name}.conf
fi

if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%files
%defattr(644,root,root,755)
%doc README scripts util
%doc docs/{CHANGES,CODING_STANDARDS,CONTRIBUTING,CREDITS,HACKING,INSTALL}
%doc docs/{PERFORMANCE,RELEASE{,_NOTES},SECURITY,TODO,TRANSLATIONS,UPGRADING}
%dir %{_sysconfdir}
%attr(750,root,http) %dir %{_sysconfdir}/%{name}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache-%{name}.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/%{name}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/%{name}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{name}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/%{name}/*.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/admin
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/js
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/services
%{_appdir}/templates
%{_appdir}/themes

%dir %attr(750,root,http) /var/log/%{name}
%ghost %attr(770,root,http) /var/log/%{name}/%{name}.log
