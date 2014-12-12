$packages = [
	'python-pip'
]

 exec { 'apt-get update':
   command => '/usr/bin/apt-get update'
 }

package { $packages:
  ensure => present,
  require => Exec['apt-get update']
}

exec { 'venv install':
	require => Package[$packages],
	ensure => present,
	command => '/usr/bin/pip install virtualenv'
}

exec { 'venv create':
	require => Exec['venv install'],
	creates => '/home/vagrant/share/.venv',
	command => 'virtualenv -p python3 /home/vagrant/share/.venv --no-site-packages'
}
