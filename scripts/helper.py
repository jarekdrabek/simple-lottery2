from brownie import accounts, network, config


def get_config():
    working_network = network.show_active()
    account = accounts.load(config['contract'][working_network]['account_name'])
    vrf_coordinator = config['contract'][working_network]['dependencies']['randomness']['vrf_coordinator']
    keyhash = config['contract'][working_network]['dependencies']['randomness']['keyhash']
    subscription_id = config['contract'][working_network]['dependencies']['randomness']['subscription_id']
    return network, account, vrf_coordinator, keyhash, subscription_id


def get_deployed_lottery_address():
    return config['contract'][network.show_active()]['address']


def get_winning_probability_in_promiles():
    return config['contract'][network.show_active()]['winning_probability_in_promiles']