from django.shortcuts import render, get_object_or_404
from web3 import Web3
from .models import Wallet, Admin_wallet
from django.contrib.auth.decorators import login_required
from pywallet import wallet
from pywallet.wallet import HDPrivateKey, HDKey
# Create your views here.

w3_ropsten = Web3.HTTPProvider('https://ropsten.infura.io/1f6867a485a04ba4b60c11522584e978')


w3 = Web3([w3_ropsten])


def create_adminwallet(request):
    ctx = {}
    if request.method == 'POST':
        seed = wallet.generate_mnemonic()
        w = wallet.create_wallet(network='ETH', seed=seed)
        coin = 'ETH'
        xpub = w['xpublic_key']
        xpriv = w['xprivate_key']
        address = w['address']
        admin_wallet = Admin_wallet.objects.create(
            seed=seed,
            coin=coin,
            xpub=xpub,
            xpriv=xpriv,
            address=address
        )
        ctx = {
            'admin_wallet': admin_wallet
        }

    return render(request, 'create_adminwallet.html', ctx)


@login_required
def create_wallet(request):
    ctx = {}
    if request.method == 'POST':
        user = request.user
        parentwallet = get_object_or_404(Admin_wallet, pk=1)
        last_wallet = Wallet.objects.last()
        master_key = HDPrivateKey.master_key_from_mnemonic(parentwallet.seed)
        root_keys = HDKey.from_path(master_key, "m/44'/60'/0'")
        acct_priv_key = root_keys[-1]
        keys = HDKey.from_path(acct_priv_key, '{change}/{index}'.format(change=0, index=last_wallet.pk))
        private_key = keys[-1]
        public_key = private_key.public_key
        w = Wallet.objects.create(
            user=user,
            parent=parentwallet,
            address=private_key.public_key.address(),
            private_key=private_key
        )
        ctx = {
            'wallet': w
        }
    return render(request, 'create_wallet.html', ctx)


@login_required
def my_wallet(request):
    if hasattr(request.user, 'wallet'):
        user = request.user
        wallet = user.wallet
        address = wallet.address
        value = w3.fromWei(w3.eth.getBalance(w3.toChecksumAddress(address)),'ether')

        ctx = {
            'wallet': wallet,
            'value': value
        }
    else:
        ctx = {'text': """계좌가 없습니다. 계좌를 만드시겠습니까?"""}
    return render(request, 'my_wallet.html', ctx)
