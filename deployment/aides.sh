#!/bin/bash
echo "Crétation du Container"
echo ""
lxc launch images:debian/stretch AidesContainerDev
echo ""

echo "Pause de 15 secondes pour laisser le container démarrer"
echo ""
for i in {0..15}; do echo -ne "$i"'\r'; sleep 1; done; echo
echo ""

echo "Apt-get Update \ upgrade"
echo ""
lxc exec AidesContainerDev -- sh -c "echo "y\n" | apt-get update"
lxc exec AidesContainerDev -- sh -c "echo "y\n" | apt-get upgrade"
echo ""

echo "Modification du passwd root (aides)"
echo ""
lxc exec AidesContainerDev -- sh -c "echo \"aides\naides\" | passwd"
echo ""

echo "Installation de ssh"
echo ""
lxc exec AidesContainerDev  -- sh -c "echo "y\n" |apt-get install ssh"
echo ""

echo "Installation de python"
echo ""
lxc exec AidesContainerDev  -- sh -c "echo "y\n" |apt-get install python"
echo ""


echo "Modification de sshd_config"
echo ""
lxc exec AidesContainerDev -- sh -c "sed -i \"s/#PermitRootLogin prohibit-password/PermitRootLogin yes/g\" /etc/ssh/sshd_config"
echo ""

echo "Redémarage du service ssh"
echo ""
lxc exec AidesContainerDev -- sh -c "/etc/init.d/ssh restart"
echo ""

echo "Génération de la clé rsa si elle n'existe pas"
echo ""
if ! [ -f "$HOME/.ssh/id_rsa" ];
then
  echo "La clé rsa n'existe pas, elle est donc généré";
  ssh-keygen -t rsa
else
  echo "La clé rsa existe, elle n'est donc  pas généré";
fi
echo ""

echo "envois de la clé rsa publique au container"
echo ""
ip=$(lxc list AidesContainerDev -c 4| awk '!/IPV4/{ if ( $2 != "" ) print $2}')
echo " L'ip du serveur est "$ip
ssh-keyscan -H $ip >> ~/.ssh/known_hosts
sshpass -p "aides" ssh-copy-id -i $HOME/.ssh/id_rsa.pub root@$ip
echo ""
echo "Fin de création et configuration du container"
echo ""


#echo "Récupération de aides-territoires depuis git"
#echo ""
#git clone -b ansible_local --single-branch https://github.com/MTES-MCT/aides-territoires
#echo ""










