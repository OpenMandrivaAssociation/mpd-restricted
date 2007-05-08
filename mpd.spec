%define __libtoolize /bin/true

%define name 	mpd
%define version 0.12.2
%define release %mkrel 1

%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}

%if %build_plf  
%define distsuffix plf
%endif


Name:			%name
Version:		%version
Release:		%release
Summary:                MPD, the Music Player Daemon
License:		GPL
Group:			Sound
URL:			http://www.musicpd.org/
Source:			http://mercury.chem.pitt.edu/~shank/%{name}-%{version}.tar.bz2
Source1:		%{name}-service.tar.bz2
Patch1:                 %{name}-0.12.1-configure-faad.patch
Patch2:			mpd-0.12.1-flac-1.1.4-support.patch
BuildRoot:		%{_tmppath}/%{name}-%{version}-buildroot
Requires(pre):		rpm-helper
Requires(post):         rpm-helper
Requires(preun):        rpm-helper
Requires(postun):       rpm-helper
BuildRequires:	        libao-devel
BuildRequires:	        libogg-devel
BuildRequires:	        libvorbis-devel
BuildRequires:	        libflac-devel libflac++-devel
BuildRequires:	        libaudiofile-devel
BuildRequires:	        libmikmod-devel
BuildRequires:	        libmad-devel
BuildRequires:	        libid3tag-devel
BuildRequires:          autoconf2.5
BuildRequires:		libatomic_ops-devel
%if %build_plf
BuildRequires:          libfaad2-devel

%description
Music Player Daemon (MPD) allows remote access for playing music (MP3, Ogg
Vorbis, FLAC, Mod, and wave files) and managing playlists. MPD is designed
for integrating a computer into a stereo system that provides control for music
playback over a local network. It is also makes a great desktop music player,
especially if your a console junkie, like frontend options, or restart X often.
This plf version of MPD add AAC files support by using libfaad2_0.

%else
%description
Music Player Daemon (MPD) allows remote access for playing music (MP3, Ogg
Vorbis, FLAC, Mod, and wave files) and managing playlists. MPD is designed
for integrating a computer into a stereo system that provides control for music
playback over a local network. It is also makes a great desktop music player,
especially if your a console junkie, like frontend options, or restart X often.
%endif

%prep
%setup -q
%patch1 -p0
%patch2 -p1 -b .newflac
autoconf

%build
%if %build_plf
%configure
%else
%configure --disable-aac
%endif
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

mkdir -p $RPM_BUILD_ROOT/var/lib/mpd
touch $RPM_BUILD_ROOT/%{_localstatedir}/mpd/mpd.db
touch $RPM_BUILD_ROOT/%{_localstatedir}/mpd/mpdstate
mkdir -p $RPM_BUILD_ROOT/var/log/mpd
touch $RPM_BUILD_ROOT/var/log/mpd/mpd.log
touch $RPM_BUILD_ROOT/var/log/mpd/mpd.error

tar xjf %{SOURCE1} -C $RPM_BUILD_DIR/%{name}-%{version}
install -D mpd.conf $RPM_BUILD_ROOT/etc/mpd.conf
install -D mpd.init $RPM_BUILD_ROOT/%{_initrddir}/%name
install -D -m 644 mpd.logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%name

rm -rf $RPM_BUILD_ROOT/%{_docdir}/mpd

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%_pre_useradd %name %{_localstatedir}/%{name} /bin/false
usermod -g audio %name


%post
if [ $1 -eq 1 ]
then
%create_ghostfile %{_localstatedir}/mpd/mpd.db mpd audio 644
%create_ghostfile %{_localstatedir}/mpd/mpdstate mpd audio 644
%create_ghostfile /var/log/mpd/mpd.log mpd audio 644
%create_ghostfile /var/log/mpd/mpd.error mpd audio 644
fi
#echo If you want to run mpd as a service, please read
#echo /usr/share/doc/mpd-%{version}/README.MDK
%_post_service %name

%preun
%_preun_service %name

%postun
%_postun_userdel %name

%files
%defattr(-,root,root)
%doc README UPGRADING doc/COMMANDS AUTHORS COPYING ChangeLog doc/mpdconf.example README.install.urpmi
%{_bindir}/%name
%{_mandir}/man1/*
%{_mandir}/man5/*
%config(noreplace) %{_sysconfdir}/logrotate.d/%name
%attr(-,mpd,root) %config(noreplace) %{_sysconfdir}/%name.conf
%config(noreplace) %{_initrddir}/%name

%defattr(644,mpd,audio)
%attr(755,mpd,audio) %dir %{_localstatedir}/mpd
%ghost %{_localstatedir}/mpd/mpd.db
%ghost %{_localstatedir}/mpd/mpdstate
%attr(755,mpd,audio) %dir /var/log/mpd
%ghost /var/log/mpd/mpd.log
%ghost /var/log/mpd/mpd.error


