Summary:	Log parsing and notification program
Summary(pl):	Program do analizy logów i powiadamiania
Name:		tenshi
Version:	0.3.4
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	http://dev.gentoo.org/~lcars/tenshi/%{name}-%{version}.tar.gz
# Source0-md5:	f3e875540833a85c43052d96c5698463
Source1:	%{name}.init
Patch0:		%{name}-root.patch
URL:		http://www.gentoo.org/proj/en/infrastructure/tenshi/index.xml
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	perl-base >= 1:5.6
Requires:	perl-modules >= 1:5.8.0
Obsoletes:	wasabi
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tenshi is a log monitoring program, designed to watch one or more log
files for lines matching user defined regular expressions and report
on the matches. The regular expressions are assigned to queues which
have an alert interval and a list of mail recipients.

Queues can be set to send a notification as soon as there is a log
line assigned to it, or to send periodic reports.

Additionally, uninteresting fields in the log lines (such as PID
numbers) can be masked with the standard regular expression grouping
operators ( ). This allows cleaner and more readable reports. All
reports are separated by hostname and all messages are condensed when
possible.

%description -l pl
Tenshi to program do monitorowania logów zaprojektowany do ogl±dania
jednego lub wiêkszej liczby plików logów pod k±tem linii pasuj±cych do
zdefiniowanych przez u¿ytkownika wyra¿eñ regularnych i raportowania
tych dopasowañ. Wyra¿enia regularne s± przypisywane do kolejek
maj±cych czêstotliwo¶æ alarmowania i listê adresatów pocztowych.

Kolejki mog± byæ konfigurowane do wysy³ania powiadomieñ zaraz po
napotkaniu linii w logu lub wysy³ania regularnych raportów.

Dodatkowo nieciekawe pola z linii logów (takie jak numery procesów)
mog± byæ pokrywane standardowymi operatorami grupowania wyra¿eñ
regularnych ( ). Daje to bardziej przejrzyste i bardziej czytelne
raporty. Wszystkie raporty s± oddzielane nazw± hosta, a wszystkie
wiadomo¶ci s± tak skondensowane, jak to tylko mo¿liwe.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man8,/etc/rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{name}.8 $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart >&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop >&2
	fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc CREDITS Changelog README
%attr(755,root,root) %{_sbindir}/*
%attr(750,root,root) %dir %{_sysconfdir}/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man8/*
