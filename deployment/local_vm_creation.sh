#!/bin/bash

set -e

echo "Création du Container"

echo "Test de la présence d'une clé publique"
echo ""
if [ $(ls -al ~/.ssh/|grep -n .pub | wc -l) = "0" ]
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
sudo lxc launch images:debian/buster $ContainerName -c security.privileged=true
echo ""

echo "Pause de 15 secondes pour laisser le container démarrer"
echo ""
for i in {0..15}; do echo -ne "$i"'\r'; sleep 1; done; echo
echo ""

echo "Apt-get Update \ upgrade"
echo ""
sudo lxc exec $ContainerName -- sh -c "apt-get -y update"
sudo lxc exec $ContainerName -- sh -c "apt-get -y upgrade"
echo ""

echo "Installation de ssh"
echo ""
sudo lxc exec $ContainerName  -- sh -c "echo "y\n" |apt-get install ssh"
echo ""

echo "Envoi de la clé publique au container"
echo ""
ip=$(lxc list $ContainerName -c 4| awk '!/IPV4/{ if ( $2 != ""  && $2 != "|" ) print $2}')
echo " L'ip du serveur est "$ip
ssh-keyscan -H $ip >> ~/.ssh/known_hosts
sudo lxc exec $ContainerName -- sh -c "mkdir /root/.ssh"
sudo lxc file push $HOME/.ssh/$rsaKey $ContainerName/root/.ssh/authorized_keys --uid=0 --gid=0
echo ""

echo "Création du répertoire partagé $(dirname $PWD)"
echo ""
sudo lxc config device add $ContainerName aides disk source=$(dirname $PWD) path=/home/aides/aides
echo ""

echo "Installation de python"
echo ""
sudo lxc exec $ContainerName  -- sh -c "apt-get -y install python"
echo ""

echo "Fin de création et configuration du container"
echo ""


echo "Il reste quelques tâches à effectuer manuellement :"

echo "Ajouter la ligne suivante dans le fichier /etc/hosts :"
echo -e "\t$ip aides-territoires.local francemobilites.aides-territoires.local"
echo ""

echo "Pour plus de facilité vous pouvez ajouter et/ou modifier ~/.ssh/config pour pendre en compte aides.local avec l'IP du container."
echo "vous pouvez utiliser le modèle suivant :"
echo ""
echo "# The local instance on a LXC virtual machine and a public ip"
echo "Host aides.local"
echo -e "\tUser root"
echo -e "\tPort 22"
echo -e "\tHostName aides-territoires.local"
echo -e "\tForwardAgent yes"
echo ""

echo "En local :"
echo ""
echo "Créer le fichier .env.local dans le répertoire aides-territoires/src/"
echo ""
echo -e "\t$ cp ../src/.env.example ../src/.env.local"
echo ""
echo "Exécution de ansible pour déployer l'application dans le container"
echo ""
echo -e "\t$ ansible-playbook -i hosts -l local site.yml"
echo ""
echo "Vous pouvez maintenant accéder à l'application via votre navigateur web."
echo "https://aides-territoires.local/"
echo ""
