Summary:	The common Horde Framework for all Horde modules
Summary(pl):	Wspólny szkielet Horde do wszystkich modu³ów Horde
Name:		horde
Version:	1.2.6
Release:	1
License:	GPL
Vendor:		The Horde Project
Group:		Applications/Mail
Group(de):	Applikationen/Post
Group(pl):	Aplikacje/Poczta
Group(pt):	Aplicações/Correio Eletrônico
Source0:	ftp://ftp.horde.org/pub/horde/tarballs/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
URL:		http://www.horde.org
Requires:	php >= 4.0.3pl1
Requires:	php-imap >= 4.0.3pl1
Requires:	php-pcre >= 4.0.3pl1
Requires:	php-gettext >= 4.0.3pl1
Requires:	php-posix >= 4.0.3pl1
Requires:	php-xml >= 4.0.3pl1
Requires:	php-mcrypt >= 4.0.3pl1
Requires:	apache >= 1.3.12
Prereq:		perl
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		apachedir	/etc/httpd
%define		apachegroup	http
%define		contentdir	/home/httpd

%description
The Horde Framework provides a common structure and interface for
Horde modules (such as IMP, a web-based mail program). This RPM is
required for all other Horde module RPMS.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with Horde and its modules) please visit http://www.horde.org/.

%description -l pl
Szkielet Horde dostarcza wspóln± strukturê oraz interfejs dla 
modu³ów Horde, takich jak IMP (obs³uga poczty poprzez www). Ten
pakiet jest wymagany dla wszystkich innych modu³ów Horde.

Projekt Horde tworzy aplikacje w PHP i dostarcza je na licencji GNU
Public License. Je¿eli chcesz siê dowiedzieæ czego¶ wiêcej (tak¿e
help do IMP'a) zajrzyj na stronê http://www.horde.org

%package mysql
Summary:	MySQL configuration for the Horde Framework
Summary(pl):	Konfiguracja MySQL dla Horde
Group:		Applications/Mail
Group(de):	Applikationen/Post
Group(pl):	Aplikacje/Poczta
Group(pt):	Aplicações/Correio Eletrônico
Requires:	horde = %{version}
Requires:	php-mysql >= 4.0.3pl1
Provides:	horde-phplib-storage
Conflicts:	horde-pgsql
Conflicts:	horde-shm

%description mysql
This RPM configures the Horde Framework to use MySQL for its PHPLIB
session storage.

%description -l pl mysql
Ten pakiet dostarcza konfiguracjê Horde do wykorzystania z MySQL.

%package pgsql
Summary:	PostgreSQL configuration for the Horde Framework
Summary(pl):	Konfiguracja PostgreSQL dla Horde
Group:		Applications/Mail
Group(de):	Applikationen/Post
Group(pl):	Aplikacje/Poczta
Group(pt):	Aplicações/Correio Eletrônico
Requires:	horde = %{version}
Requires:	php-pgsql >= 4.0.3pl1
Provides:	horde-phplib-storage
Conflicts:	horde-mysql
Conflicts:	horde-shm

%description pgsql
This RPM configures the Horde Framework to use PostgreSQL for its
PHPLIB session storage.

%description -l pl pgsql
Ten pakiet dostarcza konfiguracjê Horde do wykorzystania z PostgreSQL.

%package shm
Summary:	Shared memory configuration for the Horde Framework
Summary(pl):	Konfiguracja pamiêci dzielonej dla Horde
Group:		Applications/Mail
Group(de):	Applikationen/Post
Group(pl):	Aplikacje/Poczta
Group(pt):	Aplicações/Correio Eletrônico
Requires:	horde = %{version} 
Requires:	php-sysvsem >= 4.0.3pl1
Requires:	php-sysvshm >= 4.0.3pl1
Provides:	horde-phplib-storage
Conflicts:	horde-mysql
Conflicts:	horde-pgsql

%description shm
This RPM configures the Horde Framework to use shared memory for its
PHPLIB session storage.

%description -l pl shm
Ten pakiet konfiguruje Horde do u¿ywania pamiêci dzielonej

%prep
%setup -q

%build
perl -pi -e "s/'.*';/'hordemgr';/ if (/var\\s+\\\$(User|Password)\\s+=/);" phplib/local.inc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{apachedir},%{contentdir}/html/horde}

cp -p $RPM_SOURCE_DIR/horde.conf $RPM_BUILD_ROOT%{apachedir}
cp -pR * $RPM_BUILD_ROOT%{contentdir}/html/horde

cd $RPM_BUILD_ROOT%{contentdir}/html/horde
mv phplib ../../horde-phplib
sh install.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "Changing apache configuration"
perl -pi -e 's/$/ index.php3/ if (/DirectoryIndex\s.*index\.html/ && !/index\.php3/);' %{apachedir}/httpd.conf
grep -i 'Include.*horde.conf$' %{apachedir}/httpd.conf >/dev/null 2>&1
if [ $? -eq 0 ]; then
	perl -pi -e 's/^#+// if (/Include.*horde.conf$/i);' %{apachedir}/httpd.conf
else
	echo "Include %{apachedir}/horde.conf" >>%{apachedir}/httpd.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
        echo "Restarting httpd daemon"
	/etc/rc.d/init.d/httpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/httpd start\" to start apache http daemon."
fi

%postun
if [ $1 -eq 0 ]; then
	echo "Changing apache configuration"
	perl -pi -e 's/^/#/ if (/^Include.*horde.conf$/i);' %{apachedir}/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
	        echo "Restarting httpd daemon"
		/etc/rc.d/init.d/httpd restart 1>&2
	else
		echo "Run \"/etc/rc.d/init.d/httpd start\" to start apache http daemon."
	fi
				
fi

%post mysql
perl -pi -e 's/^#// if (/To use an SQL database/../To use shared memory/);' %{contentdir}/horde-phplib/local.inc
cat <<_EOF2_

IMPORTANT:	If you are installing for the first time, you must now
create the Horde database tables.  The following commands (run as root)
will do this:	

# mysql -p <%{contentdir}/html/horde/scripts/database/mysql_create.sql
# mysqladmin -p reload

For more information on creating the database tables, please consult
%{contentdir}/html/horde/docs/DATABASE.

_EOF2_

%post pgsql
perl -pi -e 's/^#// if (/To use an SQL database/../To use shared memory/);' %{contentdir}/horde-phplib/local.inc
perl -pi -e 's/db_mysql\.inc/db_pgsql.inc/;' %{contentdir}/horde-phplib/prepend.php3
cat <<_EOF2_

IMPORTANT:	If you are installing for the first time, you must now
create the Horde database tables.  The following commands (run as postgres)
will do this:	

$ sh %{contentdir}/html/horde/scripts/database/pgsql_cuser.sh
$ psql template1 <%{contentdir}/html/horde/scripts/database/pgsql_create.sql

For more information on creating the database tables, please consult
%{contentdir}/html/horde/docs/DATABASE.

_EOF2_

%post shm
perl -pi -e 's/^#// if (/To use shared memory/../To use LDAP/);' %{contentdir}/horde-phplib/local.inc
perl -pi -e 's/ct_sql\.inc/ct_shm.inc/;' %{contentdir}/horde-phplib/prepend.php3

%files
%defattr(644,root,root,755)
# Apache horde.conf file
%config %{apachedir}/horde.conf
# Include top level with %dir so not all files are sucked in
%dir %{contentdir}/html/horde
# Include top-level files by hand
%{contentdir}/html/horde/*.php3
%{contentdir}/html/horde/*.sh
# Include these dirs so that all files _will_ get sucked in
%{contentdir}/html/horde/graphics
%{contentdir}/html/horde/lib
%{contentdir}/html/horde/locale
%{contentdir}/html/horde/scripts
%{contentdir}/html/horde/templates
# Include phplib directory, but don't include local.inc and prepend.php3
# %config files, which are included in subpackages
%dir %{contentdir}/horde-phplib
%{contentdir}/horde-phplib/[0-9_a-km-oq-z]*
%{contentdir}/horde-phplib/page.inc
# Mark documentation files with %doc and %docdir
%doc %{contentdir}/html/horde/COPYING
%doc %{contentdir}/html/horde/README
%docdir %{contentdir}/html/horde/docs
%{contentdir}/html/horde/docs
# Mark configuration files with %config and use secure permissions
# (note that .dist files are considered software; don't mark %config)
%attr(750,root,%{apachegroup}) %dir %{contentdir}/html/horde/config
%{contentdir}/html/horde/config/*.dist
%defattr(-,root,%{apachegroup})
%config %{contentdir}/html/horde/config/*.html
%config %{contentdir}/html/horde/config/*.php3
%config %{contentdir}/html/horde/config/*.txt

%files mysql
%defattr(644,root,root,755)
%attr(640,root,%{apachegroup}) %config %{contentdir}/horde-phplib/local.inc
%config %{contentdir}/horde-phplib/prepend.php3

%files pgsql
%defattr(644,root,root,755)
%attr(640,root,%{apachegroup}) %config %{contentdir}/horde-phplib/local.inc
%config %{contentdir}/horde-phplib/prepend.php3

%files shm
%defattr(644,root,root,755)
%attr(640,root,%{apachegroup}) %config %{contentdir}/horde-phplib/local.inc
%config %{contentdir}/horde-phplib/prepend.php3
