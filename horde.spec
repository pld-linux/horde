# TODO:
# - support for Oracle and Sybase
# - trigger to change config location
# - move configs to /etc
#
%include	/usr/lib/rpm/macros.php
Summary:	The common Horde Framework for all Horde modules
Summary(es):	Elementos b�sicos do Horde Web Application Suite
Summary(pl):	Wsp�lny szkielet Horde do wszystkich modu��w Horde
Summary(pt_BR):	Componentes comuns do Horde usados por todos os m�dulos
Name:		horde
Version:	2.2.7
Release:	2.2
License:	LGPL
Vendor:		The Horde Project
Group:		Development/Languages/PHP
Source0:	ftp://ftp.horde.org/pub/horde/tarballs/%{name}-%{version}.tar.gz
# Source0-md5:	f13c20221312a0d3951687a84813167f
Source1:	%{name}.conf
Patch0:		%{name}-XML_xml2sql.patch
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

%define		apachedir	/etc/httpd
%define		hordedir	/usr/share/horde

%description
The Horde Framework provides a common structure and interface for
Horde modules (such as IMP, a web-based mail program). This RPM is
required for all other Horde module RPMS.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with Horde and its modules) please visit http://www.horde.org/ .

%description -l pl
Szkielet Horde dostarcza wsp�ln� struktur� oraz interfejs dla modu��w
Horde, takich jak IMP (obs�uga poczty poprzez WWW). Ten pakiet jest
wymagany dla wszystkich innych modu��w Horde.

Projekt Horde tworzy aplikacje w PHP i dostarcza je na licencji GNU
Public License. Je�eli chcesz si� dowiedzie� czego� wi�cej (tak�e help
do IMP-a) zajrzyj na stron� http://www.horde.org/ .

%description -l pt_BR
Este pacote prov� uma interface e estrutura comuns para os m�dulos
Horde (como IMP, um programa de webmail) e � requerido por todos os
outros m�dulos Horde.

O Projeto Horde � constitu�do por diversos aplicativos web escritos em
PHP, todos liberados sob a GPL. Para mais informa��es (incluindo ajuda
com rela��o ao Horde e seus m�dulos), por favor visite
http://www.horde.org/ .

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{apachedir} \
	$RPM_BUILD_ROOT%{hordedir}/{admin,config,graphics,lib,locale,templates,util}

cp -pR scripts docs
ln -fs $RM_BUILD_ROOT%{hordedir}/config $RPM_BUILD_ROOT%{apachedir}/horde
install	%{SOURCE1}	$RPM_BUILD_ROOT%{apachedir}/
cp -pR	*.php		$RPM_BUILD_ROOT%{hordedir}

for i in config graphics lib locale templates util; do
	cp -pR $i/*	$RPM_BUILD_ROOT%{hordedir}/$i
done
for i in config lib locale templates; do
	cp -p $i/.htaccess	$RPM_BUILD_ROOT%{hordedir}/$i
done

# Described in documentation as dangerous file...
rm $RPM_BUILD_ROOT%{hordedir}/test.php

# bit unclean..
cd $RPM_BUILD_ROOT%{hordedir}/config
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

%files
%defattr(644,root,root,755)
%doc README docs/{HACKING,CONTRIBUTING,CODING_STANDARDS,CHANGES,INSTALL,scripts}
%dir %{hordedir}
%{hordedir}/*.php
%{hordedir}/admin
%{hordedir}/graphics
%{hordedir}/lib
%{hordedir}/locale
%{hordedir}/templates
%{hordedir}/util
%{apachedir}/horde
%attr(640,root,http) %config(noreplace) %{apachedir}/horde.conf
%attr(750,root,http) %dir %{hordedir}/config
%attr(640,root,http) %{hordedir}/config/*.dist
%attr(640,root,http) %config(noreplace) %{hordedir}/config/*.php
%attr(640,root,http) %config(noreplace) %{hordedir}/config/.htaccess
