# TODO:
# - support for Oracle and Sybase
#
%include	/usr/lib/rpm/macros.php
Summary:	The common Horde Framework for all Horde modules
Summary(es):	Elementos básicos do Horde Web Application Suite
Summary(pl):	Wspólny szkielet Horde do wszystkich modu³ów Horde
Summary(pt_BR):	Componentes comuns do Horde usados por todos os módulos
Name:		horde
Version:	3.0.2
Release:	0.2
License:	LGPL
Vendor:		The Horde Project
Group:		Development/Languages/PHP
Source0:	ftp://ftp.horde.org/pub/horde/%{name}-%{version}.tar.gz
# Source0-md5:	620745a4e94dd848fff72edb3b45c184
Source1:	%{name}.conf
Patch0:		%{name}-path.patch
URL:		http://www.horde.org/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
PreReq:		apache-mod_dir >= 1.3.22
Requires(post):	grep
Requires:	apache >= 1.3.22
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

%define		hordedir	/usr/share/horde
%define		confdir		/etc/horde.org
%define		_apache2	%{?with_apache1:0}%{?!with_apache1:1}
%if %{_apache2}
%define		apachedir	/etc/httpd
Requires:	php-dom
%else
%define		apachedir	/etc/apache
Requires:	php-domxml
%endif

%description
The Horde Framework provides a common structure and interface for
Horde modules (such as IMP, a web-based mail program). This RPM is
required for all other Horde module RPMS.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with Horde and its modules) please visit http://www.horde.org/ .

%description -l pl
Szkielet Horde dostarcza wspóln± strukturê oraz interfejs dla modu³ów
Horde, takich jak IMP (obs³uga poczty poprzez WWW). Ten pakiet jest
wymagany dla wszystkich innych modu³ów Horde.

Projekt Horde tworzy aplikacje w PHP i dostarcza je na licencji GNU
Public License. Je¿eli chcesz siê dowiedzieæ czego¶ wiêcej (tak¿e help
do IMP-a) zajrzyj na stronê http://www.horde.org/ .

%description -l pt_BR
Este pacote provê uma interface e estrutura comuns para os módulos
Horde (como IMP, um programa de webmail) e é requerido por todos os
outros módulos Horde.

O Projeto Horde é constituído por diversos aplicativos web escritos em
PHP, todos liberados sob a GPL. Para mais informações (incluindo ajuda
com relação ao Horde e seus módulos), por favor visite
http://www.horde.org/ .

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{apachedir},%{confdir}/horde} \
	$RPM_BUILD_ROOT%{hordedir}/{admin,js,lib,locale,services} \
	$RPM_BUILD_ROOT%{hordedir}/{templates,themes,util}

cp -pR scripts docs
cp -pR	*.php		$RPM_BUILD_ROOT%{hordedir}

for i in admin js lib locale services templates themes util; do
	cp -pR $i/*	$RPM_BUILD_ROOT%{hordedir}/$i
done
for i in lib locale templates; do
	cp -p $i/.htaccess	$RPM_BUILD_ROOT%{hordedir}/$i
done

cp -pR config/*.php.dist	$RPM_BUILD_ROOT%{confdir}/horde
cp -p  config/.htaccess		$RPM_BUILD_ROOT%{confdir}/horde
cp -p  config/*.xml		$RPM_BUILD_ROOT%{confdir}/horde

install	%{SOURCE1}	$RPM_BUILD_ROOT%{apachedir}
ln -fs %{confdir}/%{name} $RPM_BUILD_ROOT%{hordedir}/config

# Described in documentation as dangerous file...
rm $RPM_BUILD_ROOT%{hordedir}/test.php

# bit unclean..
cd $RPM_BUILD_ROOT%{confdir}/horde
for i in *.dist; do cp $i `basename $i .dist`; done

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

cat <<_EOF2_
IMPORTANT:
If you are installing for the first time, you must now
create the Horde database tables. Look into directory
/usr/share/doc/%{name}-%{version}/scripts/db
to find out how to do this for your database.
_EOF2_

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
	    rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	fi
	if [ -f /var/lock/subsys/httpd ]; then
	    /usr/sbin/apachectl restart 1>&2
	fi
fi

%triggerpostun -- horde <= 2.2.7-2
for i in horde.php html.php lang.php mime_drivers.php mime_mapping.php motd.php prefs.php registry.php; do
	if [ -f /home/services/httpd/html/horde/config/$i.rpmsave ]; then
		cp -f %{confdir}/%{name}/$i %{confdir}/%{name}/$i.rpmnew
		mv -f /home/services/httpd/html/horde/config/$i.rpmsave %{confdir}/%{name}/$i
	fi
done
 
%files
%defattr(644,root,root,755)
%doc README docs/{HACKING,CONTRIBUTING,CODING_STANDARDS,CHANGES,INSTALL,scripts}
%dir %{hordedir}
%dir %{confdir}
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
%attr(640,root,http) %config(noreplace) %{apachedir}/horde.conf
%attr(750,root,http) %dir %{confdir}/horde
%attr(640,root,http) %{confdir}/horde/*.dist
%attr(660,root,http) %config(noreplace) %{confdir}/horde/*.php
%attr(640,root,http) %config(noreplace) %{confdir}/horde/.htaccess
%attr(660,root,http) %config(noreplace) %{confdir}/horde/*.xml
