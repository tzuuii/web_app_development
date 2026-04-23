def calculate_weakness(answers):
    """
    計算每種知識點 (topic) 的正確率，並返回分析結果。
    
    Args:
        answers (list): Answer model object list
        
    Returns:
        list: dict list 包含 topic, total, correct, accuracy, accuracy_percent
              依正確率由低至高排序
    """
    topic_stats = {}
    for ans in answers:
        if not ans.topic:
            continue
            
        topic = ans.topic
        if topic not in topic_stats:
            topic_stats[topic] = {'total': 0, 'correct': 0}
            
        topic_stats[topic]['total'] += 1
        if ans.is_correct:
            topic_stats[topic]['correct'] += 1
            
    results = []
    for topic, stats in topic_stats.items():
        accuracy = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
        results.append({
            'topic': topic,
            'total': stats['total'],
            'correct': stats['correct'],
            'accuracy': accuracy,
            'accuracy_percent': round(accuracy * 100, 1)
        })
        
    # 依正確率由低到高排序，若正確率相同則答題數多者在前
    results.sort(key=lambda x: (x['accuracy'], -x['total']))
    
    return results
