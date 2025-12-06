"""Quiz system for between maze levels"""

import pygame
import random
from src.constants import *

class Quiz:
    """Quiz manager - displays questions between levels"""
    
    def __init__(self):
        """Initialize quiz system"""
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 22)
        
        self.questions = []
        self.used_questions = []  # Track used questions this session
        self.current_question = None
        self.selected_answer = None
        self.answered = False
        self.correct = False
        
        # Load questions from file
        self.load_questions()
    
    def load_questions(self):
        """Load questions from questions.txt file"""
        try:
            with open('questions.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse question format: Question|Answer1|Answer2|Answer3|Answer4|CorrectNum
                    parts = line.split('|')
                    if len(parts) == 6:
                        question = {
                            'question': parts[0],
                            'answers': [parts[1], parts[2], parts[3], parts[4]],
                            'correct': int(parts[5]) - 1  # Convert to 0-based index
                        }
                        self.questions.append(question)
            
            print(f"Loaded {len(self.questions)} quiz questions")
        except FileNotFoundError:
            print("questions.txt not found - creating sample file")
            # Create sample questions file
            with open('questions.txt', 'w', encoding='utf-8') as f:
                f.write("# Love Maze Quiz Questions\n")
                f.write("# Format: Question|Answer1|Answer2|Answer3|Answer4|CorrectAnswerNumber\n")
                f.write("What is love?|A feeling|A choice|Both|Neither|3\n")
        except Exception as e:
            print(f"Error loading questions: {e}")
    
    def get_random_question(self):
        """Get a random question that hasn't been used this session"""
        # If all questions used, reset the pool
        if len(self.used_questions) >= len(self.questions):
            self.used_questions = []
        
        # Get unused questions
        available = [q for q in self.questions if q not in self.used_questions]
        
        if available:
            question = random.choice(available)
            self.used_questions.append(question)
            return question
        
        return None
    
    def start_quiz(self):
        """Start a new quiz question"""
        self.current_question = self.get_random_question()
        self.selected_answer = None
        self.answered = False
        self.correct = False
    
    def select_answer(self, answer_index):
        """Select an answer (0-3)"""
        if not self.answered and self.current_question:
            self.selected_answer = answer_index
            self.answered = True
            self.correct = (answer_index == self.current_question['correct'])
    
    def handle_click(self, pos):
        """Handle mouse/touch click on quiz screen"""
        if not self.current_question:
            return False
        
        x, y = pos
        
        # Answer buttons area (4 buttons stacked vertically)
        button_width = SCREEN_WIDTH - 40
        button_height = 60
        start_y = 300
        spacing = 70
        
        for i in range(4):
            button_rect = pygame.Rect(
                20,
                start_y + i * spacing,
                button_width,
                button_height
            )
            
            if button_rect.collidepoint(x, y) and not self.answered:
                self.select_answer(i)
                return True
        
        # Continue button (after answering)
        if self.answered:
            continue_rect = pygame.Rect(
                SCREEN_WIDTH // 2 - 100,
                680,
                200,
                50
            )
            if continue_rect.collidepoint(x, y):
                return True  # Signal to continue to next level
        
        return False
    
    def draw(self, screen):
        """Draw quiz screen"""
        if not self.current_question:
            return
        
        # Background
        screen.fill(LIGHT_PINK)
        
        # Title
        title = self.font_large.render("Quiz Time!", True, DARK_RED)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH // 2, top=20)
        screen.blit(title, title_rect)
        
        # Question text (wrapped if needed)
        question_text = self.current_question['question']
        self.draw_wrapped_text(screen, question_text, 20, 80, SCREEN_WIDTH - 40, PURPLE, self.font_medium)
        
        # Answer buttons
        button_width = SCREEN_WIDTH - 40
        button_height = 60
        start_y = 300
        spacing = 70
        
        for i, answer in enumerate(self.current_question['answers']):
            button_rect = pygame.Rect(20, start_y + i * spacing, button_width, button_height)
            
            # Determine button color
            if self.answered:
                if i == self.current_question['correct']:
                    color = (0, 200, 0)  # Green for correct answer
                elif i == self.selected_answer and not self.correct:
                    color = (200, 0, 0)  # Red for wrong answer
                else:
                    color = GRAY
            elif self.selected_answer == i:
                color = HOT_PINK
            else:
                color = PINK
            
            # Draw button
            pygame.draw.rect(screen, color, button_rect, border_radius=10)
            pygame.draw.rect(screen, DARK_PURPLE, button_rect, 3, border_radius=10)
            
            # Draw answer text
            answer_surf = self.font_small.render(f"{i+1}. {answer}", True, WHITE if self.answered else BLACK)
            answer_rect = answer_surf.get_rect(center=button_rect.center)
            screen.blit(answer_surf, answer_rect)
        
        # Show result after answering
        if self.answered:
            if self.correct:
                result_text = "Correct! +50 points"
                result_color = (0, 150, 0)
            else:
                result_text = "Wrong answer!"
                result_color = (150, 0, 0)
            
            result = self.font_medium.render(result_text, True, result_color)
            result_rect = result.get_rect(centerx=SCREEN_WIDTH // 2, top=630)
            screen.blit(result, result_rect)
            
            # Continue button
            continue_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 680, 200, 50)
            pygame.draw.rect(screen, PURPLE, continue_rect, border_radius=10)
            pygame.draw.rect(screen, DARK_PURPLE, continue_rect, 3, border_radius=10)
            
            continue_text = self.font_medium.render("Continue", True, WHITE)
            continue_text_rect = continue_text.get_rect(center=continue_rect.center)
            screen.blit(continue_text, continue_text_rect)
    
    def draw_wrapped_text(self, screen, text, x, y, max_width, color, font):
        """Draw text with word wrapping"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surf = font.render(test_line, True, color)
            
            if test_surf.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw lines
        for i, line in enumerate(lines):
            line_surf = font.render(line, True, color)
            screen.blit(line_surf, (x, y + i * 35))
