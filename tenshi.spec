Summary:	Log parsing and notification program
Name:		tenshi
Version:	0.3.2
Release:	0.3
License:	GPL
Group:		Applications/System
Source0:	http://dev.gentoo.org/~lcars/tenshi/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-root.patch
URL:		http://www.gentoo.org/proj/en/infrastructure/tenshi/index.xml
BuildArch:	noarch
Obsoletes:	wasabi
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tenshi is a log monitoring program, designed to watch one or more log
files for lines matching user defined regular expressions and report
on the matches. The regular expressions are assigned to queues which
have an alert interval and a list of mail recipients.

%prep
%setup -q
%patch0 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT%{_mandir}/man8 \
	$RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{name}.8 $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README INSTALL CREDITS Changelog
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
%attr(750,root,root) %dir %{_sysconfdir}/%{name}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
