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
