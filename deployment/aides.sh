#!/bin/bash

#Variables du script
ContainerName=AidesContainerLocal

echo "Création du Container"
echo ""
lxc launch images:debian/stretch $ContainerName -c security.privileged=true
echo ""

echo "Pause de 15 secondes pour laisser le container démarrer"
echo ""
for i in {0..15}; do echo -ne "$i"'\r'; sleep 1; done; echo
echo ""

echo "Apt-get Update \ upgrade"
echo ""
lxc exec $ContainerName -- sh -c "echo "y\n" | apt-get update"
lxc exec $ContainerName -- sh -c "echo "y\n" | apt-get upgrade"
echo ""

echo "Modification du passwd root (aides)"
echo ""
lxc exec $ContainerName -- sh -c "echo \"aides\naides\" | passwd"
echo ""

echo "Installation de ssh"
echo ""
lxc exec $ContainerName  -- sh -c "echo "y\n" |apt-get install ssh"
echo ""

echo "Installation de python"
echo ""
lxc exec $ContainerName  -- sh -c "echo "y\n" |apt-get install python"
echo ""


echo "Modification de sshd_config"
echo ""
lxc exec $ContainerName -- sh -c "sed -i \"s/#PermitRootLogin prohibit-password/PermitRootLogin yes/g\" /etc/ssh/sshd_config"
echo ""

echo "Redémarrage du service ssh"
echo ""
lxc exec $ContainerName -- sh -c "/etc/init.d/ssh restart"
echo ""

echo "Génération de la clé rsa, si elle n'existe pas"
echo ""
if ! [ -f "$HOME/.ssh/id_rsa" ];
then
  echo "La clé rsa n'existe pas, elle est donc générée";
  ssh-keygen -t rsa
else
  echo "La clé rsa existe, elle n'est donc  pas générée";
fi
echo ""

echo "envois de la clé rsa publique au container"
echo ""
ip=$(lxc list $ContainerName -c 4| awk '!/IPV4/{ if ( $2 != "" ) print $2}')
echo " L'ip du serveur est "$ip
ssh-keyscan -H $ip >> ~/.ssh/known_hosts
lxc exec $ContainerName -- sh -c "mkdir /root/.ssh"
lxc file push $HOME/.ssh/id_rsa.pub $ContainerName/root/.ssh/authorized_keys --uid=0 --gid=0
echo ""

echo "Ajout/Modification de ~/.ssh/config pour ajouter/modifier aides.local avec l'IP du container"
echo ""
ligne=$(grep -n "aides.local"  ~/.ssh/config | cut -d: -f1)
debut=$((ligne - 1))
fin=$((ligne + 4))
grep -n "aides.local"  ~/.ssh/config
if  [ "$?" = "0" ]
then
  echo "aides.local existe déjà."
  echo "Suppression du bloque $debut - $fin"
  sed -i " $debut , $fin d" ~/.ssh/config
  echo " Ajout de aides.local avec l'ip $ip à la fin du fichier"
  echo -e "# The local instance on a LXC virtual machine and a public ip\\nHost aides.local\\n\\tUser root\\n\\tPort 22\\n\\tHostName $ip\\n\\tForwardAgent yes" >> ~/.ssh/config
else
  echo echo "aides.local n'existe pas."
  echo "Ajout de aides.local avec l'ip $ip à la fin du fichier "
  echo -e "# The local instance on a LXC virtual machine and a public ip\\nHost aides.local\\n\\tUser root\\n\\tPort 22\\n\\tHostName $ip\\n\\tForwardAgent yes" >> ~/.ssh/config
fi
echo ""

echo "Création du répertoire partagé $(dirname $PWD)"
echo ""

lxc config device add $ContainerName aides disk source=$(dirname $PWD) path=/home/aides/aides

echo "Fin de création et configuration du container"
echo ""

echo "Exécution de ansible pour déployer l'application dans le container"
ansible-playbook -i hosts -l local -vvv site.yml
echo "Fin d'exécution de ansible"

echo "L'instalation et la configuration du container sont terminées"
echo "Il restes quelques tâches à effectuer manuellement :"
echo "En local :"
echo "- modifier \"ALLOWED_HOSTS\" dans aides-territoires/src/.env.local avec l'ip du container ($ip)"
echo ""
echo "Dans le container :"
echo "Accéder au container (ssh root@aides.local)"
echo "se loguer avec le compte aides (su aides)"
echo "Accéder au répertoire aides (cd ~/aides)"
echo "Démarrer l'environnement virtuel Python (/home/aides/.virtualenvs/aides/bin/pipenv shell)"
echo "Accéder au répertoire src (cd src)"
echo "Installer les packages python nécessaires (/home/aides/.virtualenvs/aides/bin/pipenv install --dev)"
echo "Lancer les serveur Django (python manage.py runserver 0.0.0.0:8080)"
echo "Vous pouvez maintenant accéder à l'application via votre navigateur web (ip_du_container:8080)"











