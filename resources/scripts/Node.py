class Node:
    def __init__(self, player: int, terminal: bool, eu=0.0):
        self.children = {}  # 行動をkey、子ノードをvalueとします。例えば{'check': 子ノード1, 'bet': 子ノード2}のような形になります。
        self.player = player  # このノードの手番プレイヤーです。チャンスノードの場合は-1とします。
        self.terminal = terminal  # 終端ノードの場合はTrueとなります。
        self.private_cards = []  # それぞれのプレイヤーのハンドです。
        # このノードと対応する履歴hです。ただしチャンスノードの行動、つまり手札の配り方はprivate_cardsで持つようにしてhistoryに含めないようにします。
        self.history = []
        self.information = ()  # このノードの手番プレイヤーが知ることのできる情報、つまり自身のカードとお互いの行動履歴です。
        self.pi = 0  # 履歴の到達確率π(h)です。
        self.pi_mi = 0  # π(h)のうち手番プレイヤー以外の貢献π_{-i}(h)です。
        self.pi_i = 0  # π(h)のうち手番プレイヤーのみの貢献π_{i}(h)です。平均戦略の計算に使用します。
        # ノードの期待利得u(h)です。期待利得はプレイヤー0が得られる利得とします。(プレイヤー1の利得は符号を反転させたものになります。)
        self.eu = eu
        self.cv = 0  # counterfactual valueの値です。
        self.cfr = {}  # 各行動aにおけるcounterfactual regretの累積値です。
        self.pi_i_sum = 0  # 平均戦略を計算する際の分母です。
        self.pi_sigma_sum = {}  # 平均戦略を計算する際の分子です。

    def expand_child_node(self, action: str, next_player: int, terminal: bool, utility: float = 0, private_cards=None):
        """
        self.childrenにactionをキーとして子ノードを追加します。
        子ノードの履歴は親ノードの履歴にactionを追加したもの、子ノードの情報は次のプレイヤーの手札と履歴をあわせたものになります。
        """
        next_node = Node(next_player, terminal, utility)
        self.children[action] = next_node
        self.cfr[action] = 0
        self.pi_sigma_sum[action] = 0
        # 手札は最初に配られたとき以外は前のノードのものを引き継ぎます。
        next_node.private_cards = self.private_cards if private_cards is None else private_cards
        # 前のノードがチャンスプレイヤー以外の場合はhistoryを更新します。
        next_node.history = self.history + \
            [action] if self.player != -1 else self.history
        next_node.information = (
            next_node.private_cards[next_player], tuple(next_node.history))
        return next_node


def add_list_to_dict(target_dict, key, value):
    # 同じ情報集合に属するノードをまとめるためのutility関数です。
    if key in target_dict.keys():
        target_dict[key].append(value)
    else:
        target_dict[key] = [value]


class KuhnPoker:
    def __init__(self):
        self.num_players = 2
        self.deck = [i for i in range(3)]
        # プレイヤー-1はチャンスプレイヤーを表します。
        self.information_sets = {player: {}
                                 for player in range(-1, self.num_players)}
        self.root = self._build_game_tree()

    def _build_game_tree(self):
        stack = deque()  # stackを使って深さ優先探索を行います。
        next_player = -1
        root = Node(next_player, False)
        # プレイヤー毎に同じ情報を持つノードをまとめておきます。
        add_list_to_dict(
            self.information_sets[next_player], root.information, root)
        for hand_0 in combinations(self.deck, 1):
            for hand_1 in combinations(self.deck, 1):
                if set(hand_0) & set(hand_1):  # 同じカードが配布されていた場合
                    continue
                # それぞれp0, p1, chance playerの情報です。
                private_cards = [hand_0, hand_1, ()]
                next_player = 0
                node = root.expand_child_node(str(*hand_0) + ',' + str(
                    *hand_1), next_player, False, private_cards=private_cards)  # 各行動についてノードを展開します。
                # 新しく展開したノードを適切な情報集合に加えます。
                add_list_to_dict(
                    self.information_sets[next_player], node.information, node)
                stack.append(node)
                for action in ["check", "bet"]:  # p0の取りうる行動
                    next_player = 1
                    node = node.expand_child_node(action, next_player, False)
                    add_list_to_dict(
                        self.information_sets[next_player], node.information, node)
                    stack.append(node)
                    if action == "check":
                        for action in ["check", "bet"]:  # p1の取りうる行動
                            if action == "check":
                                utility = self._compute_utility(
                                    action, next_player, hand_0, hand_1)  # p1がcheckなら利得を計算してゲーム終了です。
                                next_player = -1  # 終端ノードのプレイヤーは-1とします。
                                node = node.expand_child_node(
                                    action, next_player, True, utility)
                                add_list_to_dict(
                                    self.information_sets[next_player], node.information, node)
                                node = stack.pop()
                            if action == "bet":
                                next_player = 0
                                node = node.expand_child_node(
                                    action, next_player, False)
                                add_list_to_dict(
                                    self.information_sets[next_player], node.information, node)
                                stack.append(node)
                                for action in ["fold", "call"]:  # player 0 actions
                                    utility = self._compute_utility(
                                        action, next_player, hand_0, hand_1)
                                    next_player = -1
                                    node = node.expand_child_node(
                                        action, next_player, True, utility)
                                    add_list_to_dict(
                                        self.information_sets[next_player], node.information, node)
                                    node = stack.pop()
                    if action == "bet":
                        stack.append(node)
                        for action in ["fold", "call"]:  # player 1 actions
                            utility = self._compute_utility(
                                action, next_player, hand_0, hand_1)
                            next_player = -1
                            node = node.expand_child_node(
                                action, next_player, True, utility)
                            add_list_to_dict(
                                self.information_sets[next_player], node.information, node)
                            node = stack.pop()
        return root

    def _compute_utility(self, action, player, hand_0, hand_1):
        # ルールにしたがって利得を計算します。
        card_0, card_1 = hand_0[0], hand_1[0]
        is_win = card_0 > card_1
        if action == "fold":
            utility = 1 if player == 1 else -1
        elif action == "check":
            utility = 1 if is_win else -1
        elif action == "call":
            utility = 2 if is_win else -2
        else:
            utility = 0
        return utility
