package com.stubu.studybuddy.api.question;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class QuestionService {

    private final QuestionRepository questionRepository;

    @Autowired
    public QuestionService(QuestionRepository questionRepository) {
        this.questionRepository = questionRepository;
    }

    public List<Question> getAllQuestions() {
        return questionRepository.findAll();
    }
    public Question addQuestion(Question question) {
        // Loggen des empfangenen Question-Objekts
        System.out.println("Empfangene Frage: " + question.getQuestion());
        System.out.println("Empfangenes Kapitel: " + question.getChapter());
        return questionRepository.save(question);
    }

    public Question getQuestionById(Long id) {
        return questionRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Frage nicht gefunden")); // Hier sollten Sie eine passendere Exception wählen
    }

    public List<Question> getQuestionsByTopicId(Long topicId) {
        return questionRepository.findByTopicId(topicId);
    }

    // Weitere Methoden zur Verwaltung von Fragen hinzufügen
}