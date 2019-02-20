#!/bin/bash

echo "Création du Container"

echo "Test de la présence d'une clé publique"
echo ""
if [ $(ls -al ~/.ssh|grep -n .pub | wc -l) = "0" ]
then
  echo "Il n'existe pas de clé publique"
  echo "Il faut la générer avc la commande : ssh-keygen -t rsa"
  echo "Puis relancer le script"
  exit
else
  echo "Quelle clé publique utiliser ?"
  ls -a ~/.ssh|grep .pub
  read rsaKey
fi

if [ -e "$HOME/.ssh/"$rsaKey ]
then
  echo "la clé publique utilisée sera -> "$rsaKey
else
  echo "la clé publique saisie ($rsaKey) est incorrecte"
  echo "relancez le script"
exit
fi

echo "Donner un nom à la machine virtuelle (par défaut AidesContainerLocal)"
read ContainerName
if [ -z "$ContainerName" ]
then
  ContainerName=AidesContainerLocal
fi

echo ""
lxc launch images:debian/stretch $ContainerName -c security.privileged=true
echo ""

echo "Pause de 15 secondes pour laisser le container démarrer"
echo ""
for i in {0..15}; do echo -ne "$i"'\r'; sleep 1; done; echo
echo ""

echo "Apt-get Update \ upgrade"
echo ""
lxc exec $ContainerName -- sh -c "apt-get -y update"
lxc exec $ContainerName -- sh -c "apt-get -y upgrade"
echo ""

echo "Installation de ssh"
echo ""
lxc exec $ContainerName  -- sh -c "echo "y\n" |apt-get install ssh"
echo ""

echo "envoi de la clé publique au container"
echo ""
ip=$(lxc list $ContainerName -c 4| awk '!/IPV4/{ if ( $2 != ""  && $2 != "|" ) print $2}')
echo " L'ip du serveur est "$ip
ssh-keyscan -H $ip >> ~/.ssh/known_hosts
lxc exec $ContainerName -- sh -c "mkdir /root/.ssh"
lxc file push $HOME/.ssh/$rsaKey $ContainerName/root/.ssh/authorized_keys --uid=0 --gid=0
echo ""

echo "Création du répertoire partagé $(dirname $PWD)"
echo ""
lxc config device add $ContainerName aides disk source=$(dirname $PWD) path=/home/aides/aides
echo ""

echo "Installation de python"
echo ""
lxc exec $ContainerName  -- sh -c "apt-get -y install python"
echo ""

echo "Fin de création et configuration du container"
echo ""


echo "Il restes quelques tâches à effectuer manuellement :"

echo "Pour plus de facilité vous pouvez ajouter et/ou Modifier ~/.ssh/config pour pour pendre en compte aides.local avec l'IP du container"
echo "vous pouvez utiliser le modèle suivant :"
echo "# The local instance on a LXC virtual machine and a public ip"
echo "Host aides.local"
echo -e "\tUser root"
echo -e "\tPort 22"
echo -e "\tHostName $ip"
echo -e "\tForwardAgent yes"
echo ""

echo "En local :"
echo ""
echo "créer le fichier .env.local dans le répertoire aides-territoires/src/"
echo "SECRET_KEY='hg_1)(oo53y2ow1bvlr6k2mv#hk1lo4%6qf1pdf*02%\$203kmt'"
echo "DATABASE_URL='psql://aides:aides@localhost/aides'"
echo "ALLOWED_HOSTS=aides.local,$ip"
echo "INTERNAL_IPS=127.0.0.1,10.0.3.1"
echo "COMPRESS_OFFLINE=True"
echo "MAILING_LIST_LIST_ID=1"
echo "MAILING_LIST_FORM_ACTION=https://my.sendinblue.com/users/subscribe/js_id/blablabla/id/1"
echo ""
echo "Exécution de ansible pour déployer l'application dans le container"
echo "Lancez la commande ansible-playbook -i hosts -l local site.yml"
echo ""
echo ""
echo "Sur la machine virtuelle :"
echo "Accéder au container (ssh aides.local)"
#echo "Arrêter le superviseur (???)"
echo "se loguer avec le compte aides (su aides)"
echo "Accéder au répertoire aides (cd ~/aides)"
echo "Démarrer l'environnement virtuel Python (/home/aides/.virtualenvs/aides/bin/pipenv shell)"
echo "Accéder au répertoire src (cd src)"
echo "Installer les packages python nécessaires (/home/aides/.virtualenvs/aides/bin/pipenv install --dev)"
echo "Lancer les serveur Django (python manage.py runserver 0.0.0.0:8080)"
echo "Vous pouvez maintenant accéder à l'application via votre navigateur web ($ip:8080)"